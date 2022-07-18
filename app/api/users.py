import logging

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils import common
from app.db.get_db import get_mysql_db
from app.utils.auth import create_user_token, depend_user_access_token, login_process
from app.settings.settings import RedisConfirmType, UserRoles
from app.utils.message import EXISTING_EMAIL, INVALID_EMAIL
from app.utils.http_exception import ErrorRequestException

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/createUser",
    response_model=schemas.users.ResUserCreate,
    responses={
        500: {"model": schemas.base.ErrorResponse},
    })
async def create_user(
    schema: schemas.users.ReqCreateUser,
    authorize: dict = Depends(depend_user_access_token),
    db: Session = Depends(get_mysql_db),
):
    created_at = common.get_current_datetime()
    crud.users.check_user_role(
        db,
        user_id=authorize.get("id"),
        role_id=UserRoles.admin,
    )
    existing_user = crud.users.get_user_by_email(
        db,
        email=schema.email,
    )
    if existing_user is not None:
        raise ErrorRequestException(EXISTING_EMAIL)

    hash_password = common.get_hash_password(schema.password)
    new_user = crud.users.create_new_user(
        db,
        email=schema.email,
        password=hash_password,
        full_name=schema.fullName,
        phone=schema.phone,
        created_at=created_at,
    )
    logger.info(f"New user created: {new_user}")
    role_id = schema.roleId
    if role_id is None:
        role_id = UserRoles.user
    
    crud.users.create_user_role(
        db,
        user_id=new_user.id,
        role_id=role_id,
    )
    access_token, refresh_token = create_user_token(
        id=new_user.id,
        uuid=new_user.uuid,
    )
    new_user = new_user.__dict__
    new_user['id'] = new_user['uuid']
    return common.get_success_response(
        content={
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "userInfo": new_user,
        }
    )

@router.post(
    "/loginUser",
    response_model=schemas.users.ResUserAccessToken,
    responses={
        500: {"model": schemas.base.ErrorResponse},
    })
async def login_user(
    schema: schemas.users.ReqLoginUser,
    db: Session = Depends(get_mysql_db),
):
    user = crud.users.get_user_by_email(
        db,
        email=schema.email,
    )
    if user is None:
        raise ErrorRequestException(INVALID_EMAIL)
    access_token, refresh_token = login_process(
        user_id=user.id,
        user_uuid=user.uuid,
        user_password=user.password,
        req_password=schema.password
    )
    user = user._asdict()
    user['id'] = user['uuid']
    return common.get_success_response(
        content={
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "userInfo": user,
        }
    )



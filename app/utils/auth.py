import json
import logging

from fastapi.params import Depends
from fastapi.security import APIKeyHeader, HTTPBearer
from fastapi_jwt_auth import AuthJWT

from app.db.get_db import get_redis_db
from app.settings.settings import JWTSetting, RedisSetting
from app.utils.http_exception import ErrorRequestException, raise_exception
from app.utils.message import INVALID_ACCESS_TOKEN, INVALID_REFRESH_TOKEN
from app.utils.password import PasswordHandler

logger = logging.getLogger(__name__)

OAUTH2_TOKEN = HTTPBearer(
    auto_error=False
)

API_KEY = APIKeyHeader(
    name='API-Key',
    auto_error=False
)

REDIS_CONN = get_redis_db()

@AuthJWT.load_config
def get_config():
    return JWTSetting()

def depend_user_access_token(
    authorize: AuthJWT = Depends(),
    _oauth2_schema: str = Depends(OAUTH2_TOKEN),
):
    return verify_access_token(authorize, ["user"])

def depend_user_refresh_token(
        authorize: AuthJWT = Depends(),
        _oauth2_schema: str = Depends(OAUTH2_TOKEN)
):
    return verify_refresh_token(authorize, ["user"])

def generate_key_auth_token(raw_jwt):
    return f"/{RedisSetting().redis_prefix}/auth/{raw_jwt['sub']}/{raw_jwt['id']}/{raw_jwt['type']}_token/{raw_jwt['jti']}"

def check_existing_jwt_token(raw_jwt):
    entry = REDIS_CONN.get(generate_key_auth_token(raw_jwt))
    return entry is not None

def verify_access_token(authorize, subs):
    try:
        authorize.jwt_required()
        raw_jwt = authorize.get_raw_jwt()
        if authorize.get_jwt_subject() in subs and check_existing_jwt_token(raw_jwt):
            return raw_jwt
    except Exception as e:
        logger.info(e)
    raise ErrorRequestException(INVALID_ACCESS_TOKEN)

def verify_refresh_token(authorize, subs):
    try:
        authorize.jwt_refresh_token_required()
        raw_jwt = authorize.get_raw_jwt()
        if authorize.get_jwt_subject() in subs and check_existing_jwt_token(raw_jwt):
            return raw_jwt
    except Exception as e:
        logger.info(e)
    raise ErrorRequestException(INVALID_REFRESH_TOKEN)

def get_jwt_claims(**kwargs):
    return {
        "sub": kwargs.get('sub', None),
        "id": kwargs.get('id', None),
        "uuid": kwargs.get('uuid', None)
    }

def create_auth_tokens(
        auth_jwt,
        claims: dict
):
    access_expires_time = JWTSetting().authjwt_access_token_expires
    refresh_token = auth_jwt.create_refresh_token(
        subject=claims['sub'],
        user_claims=claims,
        expires_time=False
    )
    access_token = auth_jwt.create_access_token(
        subject=claims['sub'],
        user_claims=claims,
        expires_time=access_expires_time
    )
    create_redis_data_for_login(
        auth_jwt,
        access_token=access_token,
        refresh_token=refresh_token
    )
    return access_token, refresh_token

def create_redis_data_for_login(
        auth_jwt,
        access_token: str = None,
        refresh_token: str = None
):
    try:
        if access_token is not None:
            data = {}
            raw_jwt_access = auth_jwt.get_raw_jwt(access_token)
            if refresh_token is not None:
                raw_jwt_refresh = auth_jwt.get_raw_jwt(refresh_token)
                REDIS_CONN.set(
                    generate_key_auth_token(raw_jwt_refresh),
                    json.dumps(data)
                )
                data['jwt_refresh'] = raw_jwt_refresh['jti']
            if "exp" in raw_jwt_access:
                REDIS_CONN.setex(
                    generate_key_auth_token(raw_jwt_access),
                    JWTSetting().authjwt_access_token_expires,
                    json.dumps(data)
                )
            else:
                REDIS_CONN.set(
                    generate_key_auth_token(raw_jwt_access),
                    json.dumps(data)
                )
    except Exception as e:
        raise_exception(e)

def create_redis_data_for_refresh_token(
        auth_jwt,
        access_token: str = None,
        refresh_jti: str = None
):
    try:
        raw_jwt_access = auth_jwt.get_raw_jwt(access_token)
        data = {
            'jwt_refresh': refresh_jti
        }
        REDIS_CONN.setex(
            generate_key_auth_token(raw_jwt_access),
            raw_jwt_access['exp'],
            json.dumps(data)
        )
    except Exception as e:
        raise_exception(e)

def create_user_token(
    id: int,
    uuid: str
):
    claims = get_jwt_claims(
        sub="user",
        id=id,
        uuid=uuid
    )
    auth_jwt = AuthJWT()
    return create_auth_tokens(
        auth_jwt=auth_jwt,
        claims=claims
    )

def login_process(
    user_id: int,
    user_uuid: str,
    user_password: str,
    req_password: str
):
    try:
        PasswordHandler().verify_password(
            plain_password=req_password,
            hashed_password=user_password
        )
        access_token, refresh_token = create_user_token(
            id=user_id,
            uuid=user_uuid
        )
        return access_token, refresh_token
    except Exception as e:
        raise_exception(e)
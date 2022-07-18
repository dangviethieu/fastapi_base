import logging

from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import func
from app import crud, models
from app.utils import common
from app.utils.http_exception import ErrorRequestException, raise_exception
# from app.utils.http_exception import ErrorRequestException, raise_exception
from app.utils.message import ALREADY_ADDED, NOT_FOUND, PERMISSION_ERROR


logger = logging.getLogger(__name__)
class UsersCrud:

    def create_new_user(
        self,
        db: Session,
        email: str,
        password: str,
        full_name: str,
        phone: str,
        created_at: str,
    ):
        try:
            while True:
                unique_id = common.get_random_string(
                    prefix="C",
                    k=8,
                    lower_case=False,
                    exclude=["O", "0", "I", "J"]
                )
                if self.get_user_by_unique_id(db, unique_id) is None:
                    break
            new_user = models.AUsers(
                email=email,
                unique_id=unique_id,
                password=password,
                fullName=full_name,
                phone=phone,
                createdAt=created_at,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            raise_exception(e, db=db)

    @staticmethod
    def create_user_role(
        db: Session,
        user_id: int,
        role_id: int,
    ):
        try:
            new_user_role = models.AUsersRoles(
                userId=user_id,
                roleId=role_id,
            )
            db.add(new_user_role)
            db.commit()
        except Exception as e:
            raise_exception(e, db=db)

    @staticmethod
    def get_user_role(
        db: Session,
        user_id: int,
    ) -> models.AUsersRoles:
        try:
            return db.query(
                models.AUsersRoles.roleId
            ).filter(
                models.AUsersRoles.userId == user_id
            ).first()
        except Exception as e:
            raise_exception(e)
    
    def check_user_role(
        self,
        db: Session,
        user_id: int,
        role_id: int,
    ):
        try:
            role = self.get_user_role(db, user_id)
            if role is None or role.roleId != role_id:
                raise ErrorRequestException(PERMISSION_ERROR)
        except Exception as e:
            raise_exception(e)

    def get_user_by_email(
        self, 
        db: Session,
        email: str,
    ) -> models.AUsers:
        try:
            return self.pre_get_user_info(db).filter(
                models.AUsers.email == email
            ).first()
        except Exception as e:
            raise_exception(e)

    def get_user_by_unique_id(
            self,
            db: Session,
            unique_id: str
    ):
        try:
            return self.pre_get_user_info(db).filter(
                models.AUsers.uniqueId == unique_id
            ).first()
        except Exception as e:
            raise_exception(e)

    @staticmethod
    def pre_get_user_info(
        db: Session,
    ) -> models.AUsers:
        try:
            return db.query(
                models.AUsers.id,
                models.AUsers.uuid,
                models.AUsers.password,
                models.AUsers.email,
                models.AUsers.phone,
                models.AUsers.fullName,
                models.AUsers.interfaceLanguageCode,
                models.AUsers.uniqueId
            ).filter(
                models.AUsers.isActive == True
            )
        except Exception as e:
            raise_exception(e)

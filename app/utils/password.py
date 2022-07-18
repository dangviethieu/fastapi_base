import re

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.utils.http_exception import ErrorRequestException
from app.utils.message import INVALID_PASSWORD


class PasswordHandler:
    @property
    def pwd_context(self):
        return CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    @staticmethod
    def validate_password(password):
        regex_pattern = "(?=.{8,}).*$"
        if not re.match(regex_pattern, password):
            raise ErrorRequestException(INVALID_PASSWORD)

    def verify_password(self, plain_password, hashed_password):
        try:
            verify = False
            if plain_password is not None and hashed_password is not None:
                verify = self.pwd_context.verify(
                    secret=plain_password,
                    hash=hashed_password
                )
        except UnknownHashError:
            raise ErrorRequestException(INVALID_PASSWORD)
        if not verify:
            raise ErrorRequestException(INVALID_PASSWORD)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
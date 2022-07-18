import logging
import string
import random
from typing import Optional
from datetime import datetime, timezone

from app.utils.password import PasswordHandler

logger = logging.getLogger(__name__)


def get_success_response(
    content: Optional[any] = None,
    is_message: bool = False,
    status: bool = True,
    code: str = None,
):
    response = {
        "status": status,
    }
    if content is not None:
        if is_message is True:
            response["content"] = {
                "message": content,
            }
        else:
            response["content"] = content
    if code is not None:
        response["code"] = code
    return response

def get_current_datetime():
    return str(datetime.now().replace(tzinfo=timezone.utc))

def get_hash_password(
        password: str
):
    password_handler = PasswordHandler()
    password_handler.validate_password(
        password=password
    )
    return password_handler.get_password_hash(
        password=password
    )

def get_random_string(
        prefix: str = "",
        k: int = 8,
        upper_case: bool = True,
        lower_case: bool = True,
        digits: bool = True,
        exclude: list = None
):
    choices = ""
    if upper_case is True:
        choices += string.ascii_uppercase
    if lower_case is True:
        choices += string.ascii_lowercase
    if digits is True:
        choices += string.digits
    if exclude is not None and isinstance(exclude, list):
        for e in exclude:
            choices = choices.replace(str(e), "")
    return str(prefix) + ''.join(random.choices(choices, k=k - len(prefix)))
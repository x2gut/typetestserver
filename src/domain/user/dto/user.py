from datetime import datetime

from src.domain.common.dto.base import DTO


class BaseUser(DTO):
    username: str
    email: str


class UserCreate(DTO):
    username: str
    email: str
    password: str


class UserOauth(DTO):
    email: str
    google_id: str
    username: str
    is_active: bool = True


class UserLogin(DTO):
    username: str
    password: str


class OutputUser(DTO):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime | None = None


class UpdateUserEmail(DTO):
    password: str
    new_email: str
    user_id: int


class SendUserEmail(DTO):
    email: str
    user_id: int

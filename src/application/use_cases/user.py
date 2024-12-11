from datetime import timedelta
from typing import Dict, Tuple

from jwt import ExpiredSignatureError
from sqlalchemy.exc import IntegrityError

from src.application.exceptions.token import ExpiredSignature, InvalidTokenPayload, InvalidTokenType
from src.application.exceptions.user import InvalidCredentials
from src.application.interfaces.email_sender import IEmailSender
from src.domain.token.dto.token import AccessToken, RefreshToken
from src.domain.user.dto.user import OutputUser, UserLogin, UserCreate, UserOauth, UpdateUserEmail, SendUserEmail
from src.domain.user.exceptions.user import UserAlreadyExists, UserNotFound
from src.domain.user.use_cases.user import UserUseCase
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.repositories.user import UserRepository
from src.infrastructure.email.smtp_email_sender import SmtpEmailSender
from src.infrastructure.security.jwt_service import encode_jwt, decode_jwt
from src.infrastructure.security.password_hasher import PasswordHasher
from src.infrastructure.celery.tasks import send_verification_email


class BaseUserHandler(UserUseCase):
    def format_user(self, user: UserModel) -> OutputUser:
        return OutputUser(
            id=user.id, username=user.username, email=user.email, is_active=user.is_active, created_at=user.created_at
        )

    async def create_tokens(self, db_user: UserModel) -> Dict[str, str]:
        common_data = {
            "sub": db_user.username,
            "id": db_user.id,
            "email": db_user.email,
            "is_active": db_user.is_active,
        }

        access_token_data = {**common_data, "token_type": "access_token"}
        refresh_token_data = {**common_data, "token_type": "refresh_token"}

        access_token = await encode_jwt(payload=access_token_data, expire_time_minutes=15)
        refresh_token = await encode_jwt(payload=refresh_token_data, expire_timedelta=timedelta(days=30))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "type": "Bearer",
        }


class GetUserByUID(BaseUserHandler):
    async def __call__(self, user_id: int) -> OutputUser:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFound(f"User with id {user_id} not found")
        return self.format_user(user)


class GetUserByGoogleID(BaseUserHandler):
    async def __call__(self, google_id: str) -> OutputUser:
        user = await self.user_repo.get_by_google_id(google_id)
        if not user:
            raise UserNotFound(f"User with google id {google_id} not found")
        return self.format_user(user)


class RegisterUser(BaseUserHandler):
    async def __call__(self, user: UserCreate, password_hasher: PasswordHasher) -> OutputUser:
        if await self.user_repo.is_user_exists(user.username, user.email):
            raise UserAlreadyExists("User with such email or username already exists")

        user.password = await password_hasher.hash_password(user.password)
        new_user = await self.user_repo.save(user)
        return self.format_user(new_user)


class LoginOauthUser(BaseUserHandler):
    async def __call__(self, user: UserOauth) -> Dict[str, str]:
        db_user = await self.user_repo.get_by_google_id(user.google_id)
        if not db_user:
            db_user = await self.user_repo.save(user)
        return await self.create_tokens(db_user)


class LoginUser(BaseUserHandler):
    async def __call__(self, user: UserLogin, password_hasher: PasswordHasher) -> Dict[str, str]:
        db_user = await self.user_repo.get_by_username(user.username)
        if not db_user or not await password_hasher.verify_password(user.password, db_user.password):
            raise InvalidCredentials("Invalid username or password")
        return await self.create_tokens(db_user)


class RefreshUser(BaseUserHandler):
    async def __call__(self, refresh_token: str) -> Tuple[AccessToken, RefreshToken]:
        try:
            payload = await decode_jwt(refresh_token)
        except ExpiredSignatureError:
            raise ExpiredSignature

        if payload.get("token_type") != "refresh_token":
            raise InvalidTokenType("Expected token type - refresh_token")

        user_id = payload.get("id")
        if not user_id:
            raise InvalidTokenPayload("Invalid token payload")

        db_user = await self.user_repo.get_by_id(user_id)
        tokens = await self.create_tokens(db_user)
        return tokens.get("access_token"), refresh_token


class ChangeUserEmail(UserUseCase):
    async def __call__(self, user: UpdateUserEmail, password_hasher: PasswordHasher) -> None:
        db_user = await self.user_repo.get_by_id(user.user_id)
        if not db_user or not await password_hasher.verify_password(user.password, db_user.password):
            raise InvalidCredentials("Invalid username or password")
        try:
            await self.user_repo.change_emai(user_id=user.user_id, email=user.new_email)
        except IntegrityError:
            raise UserAlreadyExists("User with such email already exists")


class ChangeUserStatus(UserUseCase):
    async def __call__(self, user_id: int, status: bool):
        await self.user_repo.change_user_status(user_id=user_id, status=status)


class SendEmail(UserUseCase):
    async def __call__(self, user: SendUserEmail, email_sender: IEmailSender) -> None:
        send_verification_email.delay(user_id=user.user_id, to=user.email)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user: UserCreate) -> OutputUser:
        return await RegisterUser(self.user_repo)(user, PasswordHasher())

    async def login_user(self, user: UserLogin) -> Dict[str, str]:
        return await LoginUser(self.user_repo)(user, PasswordHasher())

    async def login_oauth_user(self, user: UserOauth) -> Dict[str, str]:
        return await LoginOauthUser(self.user_repo)(user)

    async def refresh_user(self, refresh_token: str) -> Tuple[AccessToken, RefreshToken]:
        return await RefreshUser(self.user_repo)(refresh_token)

    async def get_user_by_id(self, user_id: int) -> OutputUser:
        return await GetUserByUID(self.user_repo)(user_id)

    async def get_user_by_google_id(self, google_id: str) -> OutputUser:
        return await GetUserByGoogleID(self.user_repo)(google_id)

    async def change_user_email(self, user: UpdateUserEmail) -> None:
        await ChangeUserEmail(self.user_repo)(user, PasswordHasher())

    async def send_email(self, user: SendUserEmail) -> None:
        await SendEmail(self.user_repo)(user, SmtpEmailSender())

    async def change_user_status(self, user_id: int, status: bool) -> None:
        await ChangeUserStatus(self.user_repo)(user_id, status)

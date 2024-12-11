from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.dto.user import UserCreate, UserOauth
from src.infrastructure.database import Profile, Config
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.repositories.base import BaseSQLAlchemyRepository


class UserRepository(BaseSQLAlchemyRepository[UserModel]):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(UserModel, session)

    async def save(self, user: UserCreate | UserOauth) -> UserModel:
        """Save new user to database and creates a new config and a profile"""
        new_user = UserModel(**user.dict())
        self.session.add(new_user)
        await self.session.commit()

        profile = Profile(user_id=new_user.id)
        config = Config(user_id=new_user.id)
        self.session.add(profile)
        self.session.add(config)
        await self.session.commit()

        return new_user

    async def delete_user(self, user_id: int) -> None:
        await super().delete(user_id)

    async def change_emai(self, user_id: int, email: str) -> None:
        await super().update(id_=user_id, email=email)

    async def change_user_status(self, user_id: int, status: bool) -> None:
        await super().update(id_=user_id, is_active=status)

    async def get_by_id(self, user_id: int) -> UserModel | None:
        return await super().get_by_id(user_id)

    async def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        user: UserModel | None = (await self.session.execute(stmt)).scalars().one_or_none()

        return user

    async def get_by_username(self, username: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.username == username)
        user: UserModel | None = (await self.session.execute(stmt)).scalars().one_or_none()

        return user

    async def get_by_google_id(self, google_id: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.google_id == google_id)
        user: UserModel | None = (await self.session.execute(stmt)).scalars().one_or_none()

        return user

    async def is_user_exists(self, username: str, email: str) -> bool:
        stmt = select(UserModel).filter((UserModel.username == username) | (UserModel.email == email))
        result = await self.session.execute(stmt)
        return result.first() is not None

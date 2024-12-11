from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.profile import Profile
from src.infrastructure.database.repositories.base import BaseSQLAlchemyRepository


class ProfileRepository(BaseSQLAlchemyRepository[Profile]):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(Profile, session)

    async def create_profile(self, user_id: int):
        new_profile = Profile(user_id=user_id)
        self.session.add(new_profile)
        await self.session.commit()

        return new_profile

    async def get_profile_picture(self, user_id: int) -> str:
        stmt = select(Profile).where(Profile.user_id == user_id)
        profile: Profile = (await self.session.execute(stmt)).scalars().one_or_none()
        return profile.avatar_path

    async def update_profile_picture(self, profile_pic_url: str, user_id: int):
        stmt = update(Profile).where(Profile.user_id == user_id).values(avatar_path=profile_pic_url)
        await self.session.execute(stmt)
        await self.session.commit()

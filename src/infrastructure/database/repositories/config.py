from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.config.exceptions.config import ConfigDoesNotExistException
from src.infrastructure.database.models.user_config import Config
from src.infrastructure.database.repositories.base import BaseSQLAlchemyRepository
from src.domain.config.dto.config import Config as ConfigDTO


class ConfigRepository(BaseSQLAlchemyRepository[Config]):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(Config, session)

    async def create_config(self, user_id: int, config: dict | None, theme: str | None):
        new_config = Config(user_id=user_id, config=config, theme=theme)
        self.session.add(new_config)
        await self.session.commit()
        return new_config

    async def update_config(self, user_id: int, config: dict) -> None:
        if await self.get_config_by_user_id(user_id) is None:
            raise ConfigDoesNotExistException(f"Config does not exists for user {user_id}")
        stmt = update(Config).where(Config.user_id == user_id).values(config=config)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_config_by_user_id(self, user_id: int) -> ConfigDTO | None:
        stmt = select(Config).where(Config.user_id == user_id)
        config = (await self.session.execute(stmt)).scalars().one_or_none()
        return config

    async def update_theme(self, user_id: int, theme: str) -> None:
        stmt = update(Config).where(Config.user_id == user_id).values(theme=theme)
        await self.session.execute(stmt)
        await self.session.commit()

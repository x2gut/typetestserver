from src.domain.config.dto.config import Config as ConfigDTO
from src.domain.config.use_case.config import ConfigUseCase
from src.infrastructure.database.repositories.config import ConfigRepository


class CreateConfig(ConfigUseCase):
    async def __call__(self, user_id: int, config: dict | None, theme: str | None) -> ConfigDTO:
        return await self.repository.create_config(user_id, config, theme)


class UpdateConfig(ConfigUseCase):
    async def __call__(self, user_id: int, new_config: dict) -> None:
        return await self.repository.update_config(user_id, new_config)


class UpdateTheme(ConfigUseCase):
    async def __call__(self, user_id: int, new_theme: str) -> None:
        return await self.repository.update_theme(user_id, new_theme)


class GetConfig(ConfigUseCase):
    async def __call__(self, user_id: int) -> ConfigDTO | None:
        return await self.repository.get_config_by_user_id(user_id)


class ConfigService:
    def __init__(self, repository: ConfigRepository):
        self.repository = repository

    async def create_config(self, user_id: int, new_config: dict | None = None, theme: str | None = None):
        return await CreateConfig(self.repository)(user_id, new_config, theme)

    async def update_config(self, user_id: int, new_config: dict) -> None:
        return await UpdateConfig(self.repository)(user_id, new_config)

    async def update_theme(self, user_id: int, new_theme: str) -> None:
        return await UpdateTheme(self.repository)(user_id, new_theme)

    async def get_config(self, user_id: int) -> ConfigDTO | None:
        return await GetConfig(self.repository)(user_id)

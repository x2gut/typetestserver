from src.domain.common.dto.base import DTO


class BaseConfig(DTO):
    pass


class Config(BaseConfig):
    config: dict
    theme: str


class CreateConfig(BaseConfig):
    user_id: int
    config: dict
    theme: str


class UpdateConfig(BaseConfig):
    user_id: int
    config: dict


class UpdateTheme(BaseConfig):
    user_id: int
    theme: str

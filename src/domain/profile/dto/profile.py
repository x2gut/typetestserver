from src.domain.common.dto.base import DTO


class BaseProfile(DTO):
    user_id: int


class OutputProfile(BaseProfile):
    id: int
    avatar_path: str


class OutputProfilePicture(BaseProfile):
    avatar_path: str

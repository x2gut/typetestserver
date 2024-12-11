from src.domain.common.dto.base import DTO


class Token(DTO):
    pass


class AccessToken(Token):
    access_token: str


class RefreshToken(Token):
    refresh_token: str | None = None


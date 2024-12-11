from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    type: str


class SuccessRefreshResponse(BaseModel):
    message: str = Field("success", Literal=True)


class SuccessLoginResponse(BaseModel):
    message: str = Field("Login in", Literal=True)


class ErrorRefreshResponse(BaseModel):
    message: str = Field("Error refreshing token")


class SuccessLogoutResponse(BaseModel):
    message: str = Field("Logged out", Literal=True)

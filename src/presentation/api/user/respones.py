from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    pass


class SuccessEmailChangeResponse(BaseModel):
    message: str = Field("Email has been changed", Literal=True)

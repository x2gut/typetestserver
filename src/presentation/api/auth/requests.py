from typing import Annotated

from pydantic import BaseModel, Field, EmailStr


class CreateUserRequest(BaseModel):
    username: Annotated[str, Field(min_length=4, max_length=16)]
    password: Annotated[str, Field(min_length=8, max_length=24)]
    email: EmailStr


class LoginUserRequest(BaseModel):
    username: str
    password: str

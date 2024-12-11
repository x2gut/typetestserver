from pydantic import BaseModel, Field


class SuccessConfigUpdate(BaseModel):
    message: str = Field("Config has been updated", Literal=True)


class SuccessConfigCreate(BaseModel):
    message: str = Field("Config has been created", Literal=True)

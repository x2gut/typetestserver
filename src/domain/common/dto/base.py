from pydantic import BaseModel


class DTO(BaseModel):
    class Config:
        from_attributes = True

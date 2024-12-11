from pydantic import BaseModel


class UpdateProfile(BaseModel):
    user_id: int

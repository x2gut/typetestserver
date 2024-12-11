from pydantic import BaseModel, EmailStr


class UpdateUserEmailRequest(BaseModel):
    user_id: int
    new_email: EmailStr
    password: str


class SendEmailRequest(BaseModel):
    user_id: int
    email: EmailStr

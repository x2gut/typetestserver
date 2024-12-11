from pydantic.v1 import BaseSettings, Field


class EmailSmtpSettings(BaseSettings):
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = "typespaceservice@gmail.com"
    sender_password: str = Field(env="SMTP_SENDER_PASSWORD")

    class Config:
        env_file = ".env"

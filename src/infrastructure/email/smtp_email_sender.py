from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib

from src.application.interfaces.email_sender import IEmailSender
from src.config.smtp_email import EmailSmtpSettings
from src.infrastructure.security.jwt_service import encode_jwt

email_settings = EmailSmtpSettings()


class SmtpEmailSender(IEmailSender):
    def __init__(self):
        self.__smtp_server = email_settings.smtp_server
        self.__smtp_port = email_settings.smtp_port
        self.__sender_email = email_settings.sender_email
        self.__sender_password = email_settings.sender_password

    async def _generate_confirmation_token(self, user_id: int):
        payload: dict = {
            "sub": str(user_id),
        }
        token = await encode_jwt(payload=payload, expire_time_minutes=30)
        return token

    async def send_confirmation_email(self, user_id: int, to: str):
        msg = MIMEMultipart()
        msg['From'] = self.__sender_email
        msg['To'] = to
        msg['Subject'] = "Email confirmation"

        token = await self._generate_confirmation_token(user_id)

        body = MIMEText("Please confirm your email address by clicking the following link: "
                        f"http://localhost:8000/user/confirm-email?token={token} \n\n"
                        f"Link is valid for an hour")
        msg.attach(body)

        try:
            await aiosmtplib.send(msg,
                                  hostname=self.__smtp_server,
                                  port=self.__smtp_port,
                                  username=self.__sender_email,
                                  password=self.__sender_password)
        except Exception as e:
            raise e

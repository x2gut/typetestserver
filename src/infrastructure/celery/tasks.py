from asgiref.sync import async_to_sync
from .celery_app import app
from src.infrastructure.email.smtp_email_sender import SmtpEmailSender


@app.task
def send_verification_email(user_id: int, to: str):
    try:
        sender = SmtpEmailSender()
        async_to_sync(sender.send_confirmation_email)(to=to, user_id=user_id)
        return f"Email sent to {to} for user {user_id}"
    except Exception as e:
        return f"Failed to send email: {e}"

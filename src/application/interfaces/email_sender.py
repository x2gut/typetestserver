from abc import ABC, abstractmethod


class IEmailSender(ABC):
    @abstractmethod
    async def send_confirmation_email(self, user_id: int, to: str):
        raise NotImplementedError()

from src.infrastructure.database.repositories.user import UserRepository


class UserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

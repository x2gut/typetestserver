from src.infrastructure.database.repositories.profile import ProfileRepository


class ProfileUseCase:
    def __init__(self, profile_repository: ProfileRepository):
        self.profile_repository = profile_repository

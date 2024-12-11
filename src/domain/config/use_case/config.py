from src.infrastructure.database.repositories.config import ConfigRepository


class ConfigUseCase:
    def __init__(self, repository: ConfigRepository):
        self.repository = repository

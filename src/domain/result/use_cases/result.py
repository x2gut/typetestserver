from src.infrastructure.database.repositories.result import ResultRepository


class ResultUseCase:
    def __init__(self, repository: ResultRepository):
        self.repository = repository

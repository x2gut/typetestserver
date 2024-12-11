from typing import List

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.result.dto.result import Result as ResultDTO
from src.infrastructure.database.models.results_history import Result
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.repositories.base import BaseSQLAlchemyRepository


class ResultRepository(BaseSQLAlchemyRepository[Result]):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(Result, session)

    async def get_all_result(self) -> List[ResultDTO]:
        return await super().get_all()

    async def get_all_results_by_user_id(self, user_id: int, limit: int) -> List[ResultDTO]:
        query = select(Result).where(Result.user_id == user_id).limit(limit)
        return (await self.session.execute(query)).scalars().all()

    async def save_result(self, result: ResultDTO) -> ResultDTO:
        new_result = Result(**result.dict())
        self.session.add(new_result)
        await self.session.commit()
        return new_result

    async def get_best_results(self, limit: int, time: int, mode: str, words: int) -> list[ResultDTO]:
        query = select(
            Result.user_id,
            UserModel.username,
            func.max(Result.wpm).label("wpm"),
            func.max(Result.accuracy).label("accuracy"),
            func.max(Result.time).label("time"),
            func.max(Result.words).label("words"),
            func.max(Result.created_at).label("created_at"),
        ).join(UserModel, Result.user_id == UserModel.id)

        if mode == "time":
            query = query.filter(Result.time == time)
        elif mode == "words":
            query = query.filter(Result.words == words)

        query = (
            query.group_by(Result.user_id, UserModel.username)
            .order_by(desc("wpm"))
            .limit(limit)
        )

        result = await self.session.execute(query)

        return result.all()

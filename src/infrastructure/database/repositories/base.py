from typing import TypeVar, Generic, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from src.domain.common.repository.base import IBaseRepository
from src.infrastructure.database.base import Base

Model = TypeVar("Model", bound=Base)


class BaseSQLAlchemyRepository(IBaseRepository, Generic[Model]):
    def __init__(self, model: Model, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_: int) -> Model:
        query = select(self.model).where(self.model.id == id_)
        return (await self.session.execute(query)).scalars().one_or_none()

    async def get_all(self) -> List[Model]:
        query = select(self.model)
        return (await self.session.execute(query)).scalars().all()

    async def delete(self, id_: int) -> None:
        query = delete(self.model).where(self.model.id == id_)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, id_: int, **kwargs):
        query = update(self.model).where(self.model.id == id_).values(kwargs)
        await self.session.execute(query)
        await self.session.commit()

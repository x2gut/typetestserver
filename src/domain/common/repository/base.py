from abc import ABC
from typing import List


class IBaseRepository(ABC):
    async def get_by_id(self, id_: int):
        raise NotImplementedError()

    async def get_all(self) -> List:
        raise NotImplementedError()

    async def delete(self, id_: int) -> None:
        raise NotImplementedError()

    async def update(self, id_: int, **kwargs):
        raise NotImplementedError()

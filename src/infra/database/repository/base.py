from typing import Generic, TypeVar, Type

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

T = TypeVar('T', bound=DeclarativeBase)


class SqlBaseRepo(Generic[T]):

    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def model(self) -> Type[T]:
        for base in self.__class__.__orig_bases__:  # type: ignore
            if hasattr(base, '__args__') and len(base.__args__) > 0:
                return base.__args__[0]
        raise NotImplementedError("Generic type not found")

    async def _create(self, data: T) -> T | None:
        self.session.add(data)
        try:
            await self.session.commit()
            return data
        except IntegrityError:
            await self.session.rollback()
            return None

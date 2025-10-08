from sqlalchemy import select, delete

from src.application.user.dto import UserDto, CreateUserDto
from src.application.user.repository import IUseRepo

from src.infra.database.repository.base import SqlBaseRepo
from src.infra.database.model import UserDb

from src.mapper.user import UserMapper


class SqlUserRepo(SqlBaseRepo[UserDb], IUseRepo):

    async def get(self, tg_id: int) -> UserDto | None:
        query = select(self.model).where(self.model.tg_id == tg_id)
        res = await self.session.execute(query)
        user = res.scalar_one_or_none()
        return UserMapper().to_dto_from_db(user) if user is not None else None

    async def create(self, data: CreateUserDto) -> UserDto | None:
        user = await self._create(
            self.model(
                tg_id=data.tg_id,
            )
        )
        return UserMapper().to_dto_from_db(user) if user is not None else None

    async def delete(self, tg_id: int) -> bool:
        query = delete(self.model).where(self.model.tg_id == tg_id).returning(True)
        res = await self.session.execute(query)
        res = res.scalar_one_or_none()
        return res if res is not None else False

from sqlalchemy import delete, select, update

from src.infra.database.model import BotDb
from src.infra.database.repository.base import SqlBaseRepo

from src.application.bot.repository import IBotRepo
from src.application.bot.dto import CreateBotDto, BotDto

from src.mapper.bot import BotMapper


class SqlBotRepo(SqlBaseRepo[BotDb], IBotRepo):

    async def create(self, data: CreateBotDto) -> BotDto | None:
        data = await self._create(
            self.model(
                owner_tg_id=data.owner_tg_id,
                config_file_path=data.config_file_path,
                api_token=data.bot_api_token,
                username=data.username
            )
        )
        return BotMapper().from_db_to_dto(data) if data is not None else None

    async def get(self, bot_id: int) -> BotDto | None:
        res = await self.session.execute(
            select(self.model).where(self.model.id == bot_id)
        )
        bot = res.scalar_one_or_none()
        return BotMapper().from_db_to_dto(bot) if bot is not None else None

    async def get_all(self) -> list[BotDto]:
        res = await self.session.execute(
            select(self.model)
        )
        return [
            BotMapper().from_db_to_dto(bot) for bot in res.scalars().all()
        ]

    async def get_user_bots(self, owner_tg_id: int) -> list[BotDto]:
        res = await self.session.execute(
            select(self.model).where(self.model.owner_tg_id == owner_tg_id)
        )
        return [BotMapper().from_db_to_dto(bot) for bot in res.scalars().all()]

    async def delete(self, bot_id: int) -> bool:
        res = await self.session.execute(
            delete(self.model).where(self.model.id == bot_id).returning(True)
        )
        await self.session.commit()
        res = res.scalar_one_or_none()
        return res if res is not None else False

    async def update_status(self, bot_id: int, new_status: bool) -> bool:
        res = await self.session.execute(
            update(self.model)
            .where(self.model.id == bot_id)
            .values(
                status=new_status
            )
            .returning(True)
        )
        await self.session.commit()
        res = res.scalar_one_or_none()
        return res if res is not None else False

    async def get_by_bot_api_token(self, bot_api_token: str) -> BotDto | None:
        res = await self.session.execute(select(self.model).where(self.model.api_token == bot_api_token))
        bot = res.scalar_one_or_none()
        return BotMapper().from_db_to_dto(bot) if bot is not None else None

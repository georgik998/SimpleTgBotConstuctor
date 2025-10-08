from abc import ABC, abstractmethod

from src.application.bot.dto import CreateBotDto, BotDto

from src.application.constructor.dto import TgBotConfigDto


class IBotRepo(ABC):

    @abstractmethod
    async def create(self, data: CreateBotDto) -> BotDto | None:
        ...

    @abstractmethod
    async def get(self, bot_id: int) -> BotDto | None:
        ...

    @abstractmethod
    async def get_all(self) -> list[BotDto]:
        ...

    @abstractmethod
    async def delete(self, bot_id: int) -> bool:
        ...

    @abstractmethod
    async def update_status(self, bot_id: int, new_status: bool) -> bool:
        ...

    @abstractmethod
    async def get_user_bots(self, owner_tg_id: int) -> list[BotDto]:
        ...

    @abstractmethod
    async def get_by_bot_api_token(self, bot_api_token: str) -> BotDto | None:
        ...


class IBotConfigFileRepo(ABC):

    @abstractmethod
    async def create(self, data: TgBotConfigDto) -> str:
        ...

    @abstractmethod
    async def get(self, file_name: str) -> TgBotConfigDto | None:
        ...

    @abstractmethod
    async def delete(self, file_name: str):
        ...

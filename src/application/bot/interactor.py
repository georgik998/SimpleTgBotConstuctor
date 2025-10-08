from typing import Type

from src.application.bot.repository import IBotRepo, IBotConfigFileRepo
from src.application.bot.dto import (
    CreateBotDto, BotDto
)
from src.application.bot.exception import (
    BotAlreadyExistException, BotNotFoundException, IncorrectBotApiTokenException
)
from src.application.bot.service import ITgBotApiService

from src.application.constructor.interactor import BuildTgBotCommandsInteractor
from src.application.constructor.dto import (
    TgBotConfigDto
)


from src.application.deployment.interactor import StopTgBotInteractor, StartTgBotInteractor


class CreateBotInteractor:

    def __init__(
            self,
            bot_repo: IBotRepo,
            bot_config_file_repo: IBotConfigFileRepo,
            build_tg_bot_commands_interactor: BuildTgBotCommandsInteractor,
            start_tg_bot_interactor: StartTgBotInteractor
    ):
        self.bot_repo = bot_repo
        self.bot_config_file_repo = bot_config_file_repo
        self.build_tg_bot_commands_interator = build_tg_bot_commands_interactor
        self.start_tg_bot_interactor = start_tg_bot_interactor

    async def __call__(self, owner_tg_id: int, xml_content, bot_api_token: str, bot_url: str) -> BotDto:
        bot_commands = await self.build_tg_bot_commands_interator(xml_content=xml_content)
        config_file_path = await self.bot_config_file_repo.create(
            TgBotConfigDto(
                commands=bot_commands,
            )
        )
        bot = await self.bot_repo.create(
            CreateBotDto(
                owner_tg_id=owner_tg_id,
                config_file_path=config_file_path,
                bot_api_token=bot_api_token,
                username=bot_url
            )
        )
        await self.start_tg_bot_interactor(bot_id=bot.id)
        return bot


class DeleteBotInteractor:
    def __init__(
            self,
            bot_repo: IBotRepo,
            bot_config_file_repo: IBotConfigFileRepo,
            stop_tg_bot_interactor: StopTgBotInteractor
    ):
        self.bot_repo = bot_repo
        self.bot_config_file_repo = bot_config_file_repo
        self.stop_tg_bot_interactor = stop_tg_bot_interactor

    async def __call__(self, bot_id: int):
        bot = await self.bot_repo.get(bot_id)
        if bot is None:
            raise BotNotFoundException(bot_id)

        res = await self.stop_tg_bot_interactor(bot_id)

        await self.bot_config_file_repo.delete(file_name=bot.config_file_path)
        await self.bot_repo.delete(bot_id)


class GetUserBotsInteractor:

    def __init__(self, bot_repo: IBotRepo):
        self.bot_repo = bot_repo

    async def __call__(self, owner_tg_id: int) -> list[BotDto]:
        bots = await self.bot_repo.get_user_bots(owner_tg_id=owner_tg_id)
        return bots


class GetBotInteractor:
    def __init__(self, bot_repo: IBotRepo):
        self.bot_repo = bot_repo

    async def __call__(self, bot_id: int) -> BotDto:
        bot = await self.bot_repo.get(bot_id)
        if bot is None:
            raise BotNotFoundException(bot_id)
        return bot


class GetBotUsernameInteractor:

    def __init__(self, bot_repo: IBotRepo, tg_bot_api_service: Type[ITgBotApiService]):
        self.bot_repo = bot_repo
        self.tg_bot_api_service = tg_bot_api_service

    async def __call__(self, bot_api_token: str) -> str:
        username = await self.tg_bot_api_service(bot_api_token).get_bot_username()
        if username is None:
            raise IncorrectBotApiTokenException(bot_api_token)
        bot = await self.bot_repo.get_by_bot_api_token(bot_api_token)
        if bot is not None:
            raise BotAlreadyExistException(bot_api_token)
        return username

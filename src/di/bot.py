from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from dishka import Provider, Scope, provide, FromDishka

from src.application.bot.repository import IBotRepo, IBotConfigFileRepo
from src.application.bot.interactor import (
    CreateBotInteractor, GetUserBotsInteractor, GetBotUsernameInteractor, GetBotInteractor, DeleteBotInteractor
)
from src.application.bot.service import ITgBotApiService

from src.infra.database.repository.bot import SqlBotRepo
from src.infra.json_database.repository.bot import JsonBotConfigFileRepo
from src.infra.tg_bot_api import TgBotApiService
from src.application.constructor.interactor import BuildTgBotCommandsInteractor

from src.application.deployment.interactor import StartTgBotInteractor, StopTgBotInteractor


class BotRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_bot_repo(self, session: FromDishka[AsyncSession]) -> IBotRepo:
        return SqlBotRepo(session)

    @provide(scope=Scope.REQUEST)
    def provide_bot_config_file_repo(self) -> IBotConfigFileRepo:
        return JsonBotConfigFileRepo()


class BotServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_tg_bot_api_service(self) -> Type[ITgBotApiService]:
        return TgBotApiService


class BotInteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_create_bot_interactor(
            self,
            bot_repo: FromDishka[IBotRepo],
            bot_config_file_repo: FromDishka[IBotConfigFileRepo],
            build_tg_bot_commands_interactor: FromDishka[BuildTgBotCommandsInteractor],
            start_tg_bot_interactor: FromDishka[StartTgBotInteractor]
    ) -> CreateBotInteractor:
        return CreateBotInteractor(
            bot_repo=bot_repo,
            bot_config_file_repo=bot_config_file_repo,
            build_tg_bot_commands_interactor=build_tg_bot_commands_interactor,
            start_tg_bot_interactor=start_tg_bot_interactor
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_user_bots_interactor(self, bot_repo: FromDishka[IBotRepo]) -> GetUserBotsInteractor:
        return GetUserBotsInteractor(bot_repo=bot_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_bot_interactor(self, bot_repo: FromDishka[IBotRepo]) -> GetBotInteractor:
        return GetBotInteractor(bot_repo=bot_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_bot_username_interactor(
            self,
            bot_repo: FromDishka[IBotRepo],
            tg_bot_api_service: FromDishka[Type[ITgBotApiService]]
    ) -> GetBotUsernameInteractor:
        return GetBotUsernameInteractor(bot_repo=bot_repo, tg_bot_api_service=tg_bot_api_service)

    @provide(scope=Scope.REQUEST)
    def provide_del_bot_interactor(
            self,
            bot_repo: FromDishka[IBotRepo],
            bot_config_file_repo: FromDishka[IBotConfigFileRepo],
            stop_tg_bot_interactor: FromDishka[StopTgBotInteractor]
    ) -> DeleteBotInteractor:
        return DeleteBotInteractor(
            bot_repo=bot_repo,
            bot_config_file_repo=bot_config_file_repo,
            stop_tg_bot_interactor=stop_tg_bot_interactor
        )

from dishka import Provider, Scope, provide, FromDishka

from src.application.deployment.interactor import (
    StartTgBotInteractor, StartAllTgBotsInteractor, StopTgBotInteractor
)
from src.application.deployment.service import IDeployService

from src.application.bot.repository import IBotRepo


class DeploymentInteractorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_start_tg_bot_interactor(
            self,
            deploy_service: FromDishka[IDeployService],
            bot_repo: FromDishka[IBotRepo]
    ) -> StartTgBotInteractor:
        return StartTgBotInteractor(
            bot_repo=bot_repo,
            deploy_service=deploy_service
        )

    @provide(scope=Scope.REQUEST)
    def provide_stop_tg_bot_interactor(
            self,
            deploy_service: FromDishka[IDeployService],
            bot_repo: FromDishka[IBotRepo]
    ) -> StopTgBotInteractor:
        return StopTgBotInteractor(
            bot_repo=bot_repo,
            deploy_service=deploy_service
        )

    @provide(scope=Scope.REQUEST)
    def provide_start_all_tg_bots_interactor(
            self,
            bot_repo: FromDishka[IBotRepo],
            start_tg_bot_interactor: FromDishka[StartTgBotInteractor]
    ) -> StartAllTgBotsInteractor:
        return StartAllTgBotsInteractor(bot_repo=bot_repo, start_tg_bot_interactor=start_tg_bot_interactor)

from dishka import Provider, Scope, provide

from src.application.constructor.interactor import BuildTgBotCommandsInteractor


class ConstructorInteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_build_tg_bot_commands_interactor(self) -> BuildTgBotCommandsInteractor:
        return BuildTgBotCommandsInteractor()

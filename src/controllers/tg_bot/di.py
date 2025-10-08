from dishka import make_async_container

from src.di.infra import DatabaseProvider, DeploymentServiceProvider
from src.di.bot import BotRepoProvider, BotInteractorProvider, BotServiceProvider
from src.di.constructor import ConstructorInteractorProvider
from src.di.user import UserInteractorProvider, UserRepoProvider
from src.di.deployment import DeploymentInteractorProvider

from src.infra.database import postgres_settings
from src.infra.logger import Logger, tg_bot_logger_settings

dishka_container = make_async_container(
    DatabaseProvider(
        dsn=postgres_settings.POSTGRES_DSN,
        pool_size=25,
        max_overflow=10
    ),
    BotRepoProvider(), BotServiceProvider(), BotInteractorProvider(),
    ConstructorInteractorProvider(),
    UserInteractorProvider(), UserRepoProvider(),
    DeploymentInteractorProvider(), DeploymentServiceProvider()
)

logger = Logger(logs_file_path=tg_bot_logger_settings.LOGGER_TG_BOT_FILE_PATH).logger

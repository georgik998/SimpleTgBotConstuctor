from src.application.deployment.service import IDeployService
from src.application.deployment.config import deploy_service_settings
from src.application.deployment.exception import BotAlreadyLaunchedException, BotNotLaunchedException

from src.application.bot.repository import IBotRepo
from src.application.bot.exception import BotNotFoundException


class StartTgBotInteractor:
    deploy_service_settings = deploy_service_settings

    def __init__(
            self,
            deploy_service: IDeployService,
            bot_repo: IBotRepo
    ):
        self.deploy_service = deploy_service
        self.bot_repo = bot_repo

    async def __call__(self, bot_id: int):
        bot = await self.bot_repo.get(bot_id)
        if bot is None:
            raise BotNotFoundException(bot_id)
        if bot.status:
            raise BotAlreadyLaunchedException(bot_id)

        res = await self.deploy_service.start(
            bot_id,
            cmd=self.deploy_service_settings.DEPLOY_SERVICE_CMD.format(
                bot_config_json_file_path=bot.config_file_path,
                bot_api_token=bot.bot_api_token
            )
        )
        if res is False:
            raise BotAlreadyLaunchedException(bot_id)

        await self.bot_repo.update_status(bot_id=bot_id, new_status=True)


class StopTgBotInteractor:
    def __init__(
            self,
            deploy_service: IDeployService,
            bot_repo: IBotRepo
    ):
        self.deploy_service = deploy_service
        self.bot_repo = bot_repo

    async def __call__(self, bot_id: int):
        bot = await self.bot_repo.get(bot_id)
        if bot is None:
            raise BotNotFoundException(bot_id)
        if bot.status is False:
            raise BotNotLaunchedException(bot_id)

        res = await self.deploy_service.stop(bot_id)
        if res is False:
            raise BotNotLaunchedException(bot_id)

        await self.bot_repo.update_status(bot_id=bot_id, new_status=False)


class StartAllTgBotsInteractor:
    def __init__(self, bot_repo: IBotRepo, start_tg_bot_interactor: StartTgBotInteractor):
        self.start_tg_bot_interactor = start_tg_bot_interactor
        self.bot_repo = bot_repo

    async def __call__(self):
        bots = await self.bot_repo.get_all()
        for bot in bots:
            try:
                await self.start_tg_bot_interactor(bot_id=bot.id)
            except (BotNotFoundException, BotAlreadyLaunchedException):
                ...

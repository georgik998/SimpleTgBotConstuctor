import asyncio
from typing import Callable, Awaitable

from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from src.controllers.tg_bot.config import TelegramBotSettings
from src.controllers.tg_bot.di import logger

from src.application.deployment.interactor import StartAllTgBotsInteractor


async def on_startup(container: AsyncContainer):
    logger.info('Start on_startup...')

    logger.info('Start deploy tg_bots...')
    async with container() as request_container:
        start_all_tg_bots_interactor = await request_container.get(StartAllTgBotsInteractor)
    await start_all_tg_bots_interactor()
    logger.info('Finish deploy tg_bots!')

    logger.info('Finish on_startup!')


async def main(
        bot_settings: TelegramBotSettings,
        router: Router,
        dishka_container: AsyncContainer,
        on_startup_func: Callable[[AsyncContainer], Awaitable[None]]
):
    dp = Dispatcher()
    bot = Bot(
        token=bot_settings.TG_BOT_API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook()
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="/start",
                description="⚙️ Перезапустить бота"
            ),
        ]
    )

    dp.include_router(router)
    setup_dishka(container=dishka_container, router=dp)

    async def shutdown_wrapper():
        await dishka_container.close()

    async def startup_wrapper():
        await on_startup_func(dishka_container)

    dp.shutdown.register(shutdown_wrapper)
    dp.startup.register(startup_wrapper)

    logger.info('Start polling bot...')
    await dp.start_polling(
        bot,
        drop_pending_updates=True
    )

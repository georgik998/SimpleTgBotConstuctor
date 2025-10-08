import asyncio

from src.controllers.tg_bot.app import main, on_startup
from src.controllers.tg_bot.config import telegram_bot_settings
from src.controllers.tg_bot.handler.base.router import router
from src.controllers.tg_bot.di import dishka_container

if __name__ == '__main__':
    try:
        asyncio.run(
            main(
                bot_settings=telegram_bot_settings,
                router=router,
                dishka_container=dishka_container,
                on_startup_func=on_startup
            )
        )
    except KeyboardInterrupt:
        ...

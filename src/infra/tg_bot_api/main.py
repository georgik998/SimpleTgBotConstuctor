from aiogram import Bot
from aiogram.utils.token import TokenValidationError

from src.application.bot.service import ITgBotApiService


class TgBotApiService(ITgBotApiService):

    async def get_bot_username(self) -> str | None:
        token = self.bot_api_token
        try:
            async with Bot(token) as bot:
                me = await bot.get_me()
            return me.username
        except TokenValidationError:
            return None

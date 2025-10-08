from aiogram.filters.callback_data import CallbackData

from src.controllers.tg_bot.handler.public.base.callback import prefix

prefix = prefix + 'main'


class BackToStartCall(CallbackData, prefix=prefix + 'back'):
    ...


class DeleteBotCall(CallbackData, prefix=prefix + 'del'):
    bot_id: int


class ConfirmDelBotCall(CallbackData, prefix=prefix + 'del-confirm'):
    bot_id: int
    action: bool


class CreateBotCall(CallbackData, prefix=prefix + 'create'):
    ...

import json

from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from src.mapper.bot import BotConfigMapper


async def main(bot_config_json_file_path: str, bot_api_token: str):
    with open(bot_config_json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    config = BotConfigMapper().from_dict_to_dto(data)

    router = Router()

    @router.message(F.text == '/start')
    async def start_cmd(message: Message):
        await message.answer(
            text=config.commands.start.text,
            reply_markup=InlineKeyboardMarkup(**config.commands.start.reply_markup)
        )

    @router.callback_query(F.data == config.commands.start.callback)
    async def back_to_start_cmd(call: CallbackQuery):
        await call.message.edit_text(
            text=config.commands.start.text,
            reply_markup=InlineKeyboardMarkup(**config.commands.start.reply_markup)
        )

    @router.callback_query()
    async def handler_callback_cmd(call: CallbackQuery):
        callback_data = call.data
        if config.commands.callbacks.get(callback_data) is None:
            await call.answer('Ошибка', show_alert=True)
            return

        if config.commands.callbacks[callback_data].reply_markup is None:
            keyboard = None
        else:
            keyboard = InlineKeyboardMarkup(**config.commands.callbacks[callback_data].reply_markup)

        await call.message.edit_text(
            text=config.commands.callbacks[callback_data].text,
            reply_markup=keyboard
        )

    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(bot_api_token)
    await dp.start_polling(
        bot,
        drop_pending_updates=True
    )

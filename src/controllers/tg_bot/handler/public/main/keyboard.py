from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.controllers.tg_bot.handler.base.keyboard import build_add_element_button_text, back_button_text

from src.controllers.tg_bot.handler.public.main import callback

from src.application.bot.dto import BotDto


def build_manage_bot_kb(bots: list[BotDto]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text=f'{i}. {bot.username}',
                                    url=f'https://t.me/{bot.username}'
                                ),
                                InlineKeyboardButton(
                                    text='🗑',
                                    callback_data=callback.DeleteBotCall(
                                        bot_id=bot.id
                                    ).pack()
                                )
                            ] for i, bot in enumerate(bots, 1)
                        ] + [
                            [
                                InlineKeyboardButton(
                                    text=build_add_element_button_text('Добавить бота'),
                                    callback_data=callback.CreateBotCall().pack()
                                )
                            ]
                        ]
    )


back_to_manage_bots = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=back_button_text,
                callback_data=callback.BackToStartCall().pack()
            )
        ]
    ]
)


def build_confirm_del_bot_kb(bot_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text='Да',
                                    callback_data=callback.ConfirmDelBotCall(bot_id=bot_id, action=True).pack()
                                ),
                                InlineKeyboardButton(
                                    text='Нет',
                                    callback_data=callback.ConfirmDelBotCall(bot_id=bot_id, action=False).pack()
                                )
                            ],

                        ] + back_to_manage_bots.inline_keyboard
    )


def build_success_create_bot_kb(bot_url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(text='Бот', url=bot_url)
                            ]
                        ] + back_to_manage_bots.inline_keyboard
    )

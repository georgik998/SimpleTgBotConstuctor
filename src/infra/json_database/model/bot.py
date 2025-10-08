from typing import TypedDict


class InlineKeyboardButtonDict(TypedDict):
    text: str
    url: None
    callback_data: str
    web_app: None
    login_url: None
    switch_inline_query: None
    switch_inline_query_current_chat: None
    switch_inline_query_chosen_chat: None
    copy_text: None
    callback_game: None
    pay: None


class InlineKeyboardMarkupDict(TypedDict):
    inline_keyboard: list[list[InlineKeyboardButtonDict]]


class TgBotCallbackDict(TypedDict):
    text: str
    reply_markup: InlineKeyboardMarkupDict | None


class TgBotStartCommandDict(TypedDict):
    text: str
    reply_markup: InlineKeyboardMarkupDict | None
    callback: str


class TgBotCommandsDict(TypedDict):
    callbacks: dict[str, TgBotCallbackDict]
    start: TgBotStartCommandDict


class TgBotConfigDict(TypedDict):
    commands: TgBotCommandsDict

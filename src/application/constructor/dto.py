from __future__ import annotations
from dataclasses import dataclass
from typing import TypedDict


@dataclass
class NodeDto:
    id: str
    value: str | None


@dataclass
class Edge:
    id: str
    value: str | None
    source: str
    target: str


@dataclass
class ParsedDto:
    nodes: list[NodeDto]
    edges: list[Edge]


# ==== TREE ==== #
@dataclass
class TreeNodeDto:
    value: str
    elements: list[TreeEdgeDto] | None


@dataclass
class TreeEdgeDto:
    value: str
    element: TreeNodeDto


# ==== TgBotConfig ==== #
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


@dataclass
class TgBotCallbackDto:
    text: str
    reply_markup: InlineKeyboardMarkupDict | None


@dataclass
class TgBotStartDto:
    text: str
    reply_markup: InlineKeyboardMarkupDict | None
    callback: str


@dataclass
class TgBotCommandsDto:
    callbacks: dict[str, TgBotCallbackDto]
    start: TgBotStartDto


@dataclass
class TgBotConfigDto:
    commands: TgBotCommandsDto

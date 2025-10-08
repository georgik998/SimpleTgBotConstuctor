from dataclasses import dataclass


@dataclass
class BotDto:
    id: int
    bot_api_token: str
    username: str
    owner_tg_id: int
    status: bool
    config_file_path: str


@dataclass
class CreateBotDto:
    owner_tg_id: int
    config_file_path: str
    bot_api_token: str
    username: str

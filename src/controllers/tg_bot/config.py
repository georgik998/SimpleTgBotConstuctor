from pydantic_settings import BaseSettings
from src.config import SETTINGS_CONFIG_DICT


class TelegramBotSettings(BaseSettings):
    model_config = SETTINGS_CONFIG_DICT

    TG_BOT_API_TOKEN: str


telegram_bot_settings = TelegramBotSettings()

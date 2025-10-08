from pydantic_settings import BaseSettings

from src.config import SETTINGS_CONFIG_DICT


class TgBotLoggerSettings(BaseSettings):
    model_config = SETTINGS_CONFIG_DICT

    LOGGER_TG_BOT_FILE_PATH: str = 'src/resources/logs/tg_bot.log'


tg_bot_logger_settings = TgBotLoggerSettings()

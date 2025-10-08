from pydantic_settings import BaseSettings

from src.config import SETTINGS_CONFIG_DICT


class DeployServiceSettings(BaseSettings):
    model_config = SETTINGS_CONFIG_DICT

    DEPLOY_SERVICE_CMD: str = 'py -m src.controllers.construct_tg_bot {bot_config_json_file_path} {bot_api_token}'


deploy_service_settings = DeployServiceSettings()

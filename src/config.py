from pydantic_settings import SettingsConfigDict

SETTINGS_CONFIG_DICT = SettingsConfigDict(
    env_file='.env',
    env_file_encoding='utf-8',
    extra='allow'
)




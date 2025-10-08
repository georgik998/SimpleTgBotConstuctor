from uuid import uuid4

from src.infra.json_database.repository.base import JsonBaseRepo
from src.infra.json_database.model.bot import TgBotConfigDict

from src.application.bot.repository import IBotConfigFileRepo

from src.application.constructor.dto import TgBotConfigDto

from src.mapper.bot import BotConfigMapper

BOT_CONFIG_FILE_DIR_PATH = 'src/resources/storage/bot_config'


class JsonBotConfigFileRepo(JsonBaseRepo, IBotConfigFileRepo):
    dir_path = BOT_CONFIG_FILE_DIR_PATH
    model = TgBotConfigDict

    async def create(self, data: TgBotConfigDto) -> str:
        file_path = self.dir_path + f'/{uuid4()}.json'
        self._write(
            data=BotConfigMapper().from_dto_to_dict(data),
            file_path=file_path
        )
        return file_path

    async def get(self, file_name: str) -> TgBotConfigDto | None:
        data: TgBotConfigDict = self._get(file_name)
        if not self.model_type_matching(data):
            return None
        return BotConfigMapper().from_dict_to_dto(data) if data is not None else None

    async def delete(self, file_name: str):
        self._delete(file_name)

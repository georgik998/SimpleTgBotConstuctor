from src.infra.json_database.model.bot import (
    TgBotConfigDict, TgBotCommandsDict, TgBotStartCommandDict, TgBotCallbackDict
)
from src.application.constructor.dto import (
    TgBotCallbackDto, TgBotStartDto, TgBotCommandsDto, TgBotConfigDto,

)

from src.application.bot.dto import BotDto
from src.infra.database.model import BotDb


class BotMapper:

    @staticmethod
    def from_db_to_dto(db: BotDb) -> BotDto:
        return BotDto(
            id=db.id,
            bot_api_token=db.api_token,
            owner_tg_id=db.owner_tg_id,
            status=db.status,
            config_file_path=db.config_file_path,
            username=db.username
        )


class BotConfigMapper:

    @staticmethod
    def from_dict_to_dto(db: TgBotConfigDict) -> TgBotConfigDto:
        return TgBotConfigDto(
            commands=TgBotCommandsDto(
                callbacks={
                    key: TgBotCallbackDto(
                        text=value['text'],
                        reply_markup=value['reply_markup']
                    ) for key, value in db['commands']['callbacks'].items()
                },
                start=TgBotStartDto(
                    text=db['commands']['start']['text'],
                    reply_markup=db['commands']['start']['reply_markup'],
                    callback=db['commands']['start']['callback']
                )
            )
        )

    @staticmethod
    def from_dto_to_dict(dto: TgBotConfigDto) -> TgBotConfigDict:
        return TgBotConfigDict(
            commands=TgBotCommandsDict(
                callbacks={
                    key: TgBotCallbackDict(
                        text=callback.text,
                        reply_markup=callback.reply_markup
                    ) for key, callback in dto.commands.callbacks.items()
                },
                start=TgBotStartCommandDict(
                    text=dto.commands.start.text,
                    reply_markup=dto.commands.start.reply_markup,
                    callback=dto.commands.start.callback
                )
            )
        )

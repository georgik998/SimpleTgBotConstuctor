from src.infra.database.model import UserDb
from src.application.user.dto import UserDto


class UserMapper:

    @staticmethod
    def to_dto_from_db(db: UserDb) -> UserDto:
        return UserDto(
            tg_id=db.tg_id
        )

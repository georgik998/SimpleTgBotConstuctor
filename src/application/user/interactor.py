from src.application.user.dto import UserDto, CreateUserDto
from src.application.user.exception import UserAlreadyExistException
from src.application.user.repository import IUseRepo


class CreateUserInteractor:

    def __init__(self, user_repo: IUseRepo):
        self.user_repo = user_repo

    async def __call__(self, data: CreateUserDto) -> UserDto:
        user = await self.user_repo.create(data)
        if user is None:
            raise UserAlreadyExistException(tg_id=data.tg_id)
        return user

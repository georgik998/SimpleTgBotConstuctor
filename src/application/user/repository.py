from abc import ABC, abstractmethod

from src.application.user.dto import UserDto, CreateUserDto


class IUseRepo(ABC):

    @abstractmethod
    async def get(self, tg_id: int) -> UserDto | None:
        ...

    @abstractmethod
    async def create(self, data: CreateUserDto) -> UserDto | None:
        ...

    @abstractmethod
    async def delete(self, tg_id: int) -> bool:
        ...

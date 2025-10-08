from abc import ABC, abstractmethod


class IDeployService(ABC):

    @abstractmethod
    async def start(self, bot_id: int, cmd: str) -> bool:
        ...

    @abstractmethod
    async def stop(self, bot_id: int) -> bool:
        ...

    # @abstractmethod
    # async def get_status(self, bot_id: int) -> bool:
    #     """
    #     Получить статус процесса - работает/остановлен
    #     """

from abc import ABC, abstractmethod


class ITgBotApiService(ABC):
    def __init__(self, bot_api_token: str):
        self.bot_api_token = bot_api_token

    @abstractmethod
    async def get_bot_username(self) -> str | None:
        ...

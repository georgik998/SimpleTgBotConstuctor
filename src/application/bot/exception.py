class BotNotFoundException(Exception):
    def __init__(self, bot_id: int):
        super().__init__(f'Bot with bot_id={bot_id} not found')


class IncorrectBotApiTokenException(Exception):
    def __init__(self, bot_api_token: str):
        super().__init__(f'Bot_api_token={bot_api_token} is incorrect')


class BotAlreadyExistException(Exception):
    def __init__(self, bot_api_token: str):
        super().__init__(f'Bot with bot_api_token={bot_api_token} already exist')

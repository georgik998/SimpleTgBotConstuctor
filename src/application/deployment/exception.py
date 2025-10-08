class BotAlreadyLaunchedException(Exception):
    def __init__(self, bot_id: int):
        super().__init__(f'Bot with id={bot_id} already launched')


class BotNotLaunchedException(Exception):
    def __init__(self, bot_id: int):
        super().__init__(f'Bot with id={bot_id} not launched')

from aiogram.fsm.state import State, StatesGroup


class CreateBotState(StatesGroup):
    xml_file = State()
    bot_api_token = State()

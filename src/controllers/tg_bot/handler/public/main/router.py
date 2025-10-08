from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from dishka.integrations.aiogram import FromDishka, inject

from src.controllers.tg_bot.handler.public.main import keyboard
from src.controllers.tg_bot.handler.public.main import callback
from src.controllers.tg_bot.handler.public.main import fsm_state

from src.controllers.tg_bot.handler.base.utils import get_yaml_text

from src.application.user.interactor import CreateUserInteractor
from src.application.user.exception import UserAlreadyExistException
from src.application.user.dto import CreateUserDto

from src.application.bot.interactor import (
    GetUserBotsInteractor, GetBotInteractor, DeleteBotInteractor, GetBotUsernameInteractor, CreateBotInteractor
)
from src.application.bot.exception import (
    BotAlreadyExistException, BotNotFoundException, IncorrectBotApiTokenException
)

from src.application.constructor.exception import IncorrectXmlFileException

router = Router()

YAML_TEXT_FILE_PATH = 'src/controllers/tg_bot/handler/public/main/text.yaml'


@router.message(F.text == '/start')
@inject
async def start_cmd(
        message: Message,
        state: FSMContext,
        create_user_interactor: FromDishka[CreateUserInteractor],
        get_user_bots_interactor: FromDishka[GetUserBotsInteractor]
):
    try:
        await create_user_interactor(
            data=CreateUserDto(
                tg_id=message.from_user.id
            )
        )
    except UserAlreadyExistException:
        ...
    bots = await get_user_bots_interactor(owner_tg_id=message.from_user.id)

    await state.clear()
    await message.answer(
        text=get_yaml_text(
            YAML_TEXT_FILE_PATH, 'start'
        ),
        reply_markup=keyboard.build_manage_bot_kb(bots)
    )


@router.callback_query(
    callback.BackToStartCall.filter(),
    StateFilter(
        default_state,
        fsm_state.CreateBotState
    )
)
@inject
async def start_throw_call_cmd(
        call: CallbackQuery,
        state: FSMContext,
        get_user_bots_interactor: FromDishka[GetUserBotsInteractor]
):
    bots = await get_user_bots_interactor(owner_tg_id=call.from_user.id)

    await state.clear()
    await call.message.edit_text(
        text=get_yaml_text(
            YAML_TEXT_FILE_PATH, 'start'
        ),
        reply_markup=keyboard.build_manage_bot_kb(bots)
    )


# del
@router.callback_query(callback.DeleteBotCall.filter(), StateFilter(default_state))
@inject
async def delete_bot_cmd(
        call: CallbackQuery,
        callback_data: callback.DeleteBotCall,
        get_bot_interactor: FromDishka[GetBotInteractor],
        get_user_bots_interactor: FromDishka[GetUserBotsInteractor]
):
    try:
        bot = await get_bot_interactor(bot_id=callback_data.bot_id)
    except BotNotFoundException:
        bots = await get_user_bots_interactor(owner_tg_id=call.from_user.id)
        await call.answer(get_yaml_text(YAML_TEXT_FILE_PATH, 'exc', 'bot_not_found'))
        await call.message.edit_text(
            text=get_yaml_text(
                YAML_TEXT_FILE_PATH, 'start'
            ),
            reply_markup=keyboard.build_manage_bot_kb(bots)
        )
        return

    await call.message.edit_text(
        text=get_yaml_text(
            YAML_TEXT_FILE_PATH, 'del_bot', 'confirm'
        ).format(
            bot_username=bot.username
        ),
        reply_markup=keyboard.build_confirm_del_bot_kb(bot_id=callback_data.bot_id)
    )


@router.callback_query(callback.ConfirmDelBotCall.filter(), StateFilter(default_state))
@inject
async def confirm_delete_bot_cmd(
        call: CallbackQuery,
        callback_data: callback.ConfirmDelBotCall,
        delete_bot_interactor: FromDishka[DeleteBotInteractor],
        get_user_bots_interactor: FromDishka[GetUserBotsInteractor]
):
    if callback_data.action:
        try:
            await delete_bot_interactor(bot_id=callback_data.bot_id)
        except BotNotFoundException:
            await call.answer(get_yaml_text(YAML_TEXT_FILE_PATH, 'exc', 'bot_not_found'))

    bots = await get_user_bots_interactor(owner_tg_id=call.from_user.id)

    await call.answer(
        get_yaml_text(
            YAML_TEXT_FILE_PATH, 'del_bot', 'success'
        ) if callback_data.action else get_yaml_text(
            YAML_TEXT_FILE_PATH, 'del_bot', 'cancel'
        )
    )
    await call.message.edit_text(
        text=get_yaml_text(YAML_TEXT_FILE_PATH, 'start'),
        reply_markup=keyboard.build_manage_bot_kb(bots)
    )


# create
@router.callback_query(callback.CreateBotCall.filter(), StateFilter(default_state))
async def start_create_bot_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(fsm_state.CreateBotState.bot_api_token)
    await call.message.edit_text(
        text=get_yaml_text(
            YAML_TEXT_FILE_PATH, 'create', 'accept_api_token'
        ),
        reply_markup=keyboard.back_to_manage_bots
    )


@router.message(StateFilter(fsm_state.CreateBotState.bot_api_token), F.text)
@inject
async def accept_bot_api_token_create_bot_cmd(
        message: Message,
        state: FSMContext,
        get_bot_username_interactor: FromDishka[GetBotUsernameInteractor]
):
    bot_api_token = message.text
    try:
        username = await get_bot_username_interactor(bot_api_token)
    except IncorrectBotApiTokenException:
        await message.answer(
            get_yaml_text(YAML_TEXT_FILE_PATH, 'exc', 'incorrect_api_token'),
            reply_markup=keyboard.back_to_manage_bots
        )
        return
    except BotAlreadyExistException:
        await message.answer(
            get_yaml_text(YAML_TEXT_FILE_PATH, 'exc', 'bot_already_exist'),
            reply_markup=keyboard.back_to_manage_bots
        )
        return

    await state.update_data({'bot_api_token': bot_api_token, 'username': username})
    await state.set_state(fsm_state.CreateBotState.xml_file)
    await message.answer(
        get_yaml_text(YAML_TEXT_FILE_PATH, 'create', 'accept_xml_file'),
        reply_markup=keyboard.back_to_manage_bots
    )


@router.message(StateFilter(fsm_state.CreateBotState.xml_file), F.document)
@inject
async def accept_xml_file_create_bot_cmd(
        message: Message,
        state: FSMContext,
        bot: Bot,
        create_bot_interactor: FromDishka[CreateBotInteractor]
):
    if not message.document.file_name.endswith('.xml'):
        await message.answer(
            get_yaml_text(YAML_TEXT_FILE_PATH, 'create', 'exc', 'xml_file_format'),
            reply_markup=keyboard.back_to_manage_bots
        )
        return
    data = await state.get_data()
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    file_content = downloaded_file.read().decode('utf-8')

    try:
        await create_bot_interactor(
            owner_tg_id=message.from_user.id,
            xml_content=file_content,
            bot_api_token=data['bot_api_token'],
            bot_url=data['username']
        )
    except IncorrectXmlFileException:
        await message.answer(
            get_yaml_text(YAML_TEXT_FILE_PATH, 'create', 'exc', 'incorrect_xml_file'),
            reply_markup=keyboard.back_to_manage_bots
        )
        return

    await message.answer(
        get_yaml_text(YAML_TEXT_FILE_PATH, 'create', 'success'),
        reply_markup=keyboard.build_success_create_bot_kb(f"https://t.me/{data['username']}")
    )
    await state.clear()

from aiogram import Router

from src.controllers.tg_bot.handler.public.main.router import router as main_router

router = Router()

router.include_routers(
    main_router
)

from aiogram import Router

from src.controllers.tg_bot.handler.public.base.router import router as public_router

router = Router()

router.include_router(public_router)

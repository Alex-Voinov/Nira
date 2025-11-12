from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Это production-ready старт для Aiogram 3.\n"
        "Отправь /help чтобы посмотреть возможности."
    )

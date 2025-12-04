from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from config import settings

router = Router()

web_app_button = KeyboardButton(
    text="Регистрация",
    web_app=WebAppInfo(url=settings.web_app_url)  
)

keyboard = ReplyKeyboardMarkup(
    keyboard=[[web_app_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! ✨ Рады видеть тебя здесь.\n"
        "Нажми кнопку ниже, чтобы зарегистрироваться и открыть наш уютный мир знакомств прямо в Telegram 💌",
        reply_markup=keyboard
    )

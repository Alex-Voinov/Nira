from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from config import settings
from bot.utils.typing import send_typing
from bot.utils.message_cleaner import clean_old_messages
from bot.utils.message_storage import message_storage

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
async def cmd_start(message: types.Message, bot: Bot):

    # 1. Удаляем старые сообщения бота
    await clean_old_messages(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        bot=bot,
        storage=message_storage
    )

    # 2. Анимация "печатает..."
    await send_typing(bot, message.chat.id, seconds=1.4)

    # 3. Новое сообщение
    await message.answer(
        "Привет! ✨ Рады видеть тебя здесь.\n"
        "Нажми кнопку ниже, чтобы зарегистрироваться и открыть наш уютный мир знакомств прямо в Telegram 💌",
        reply_markup=keyboard
    )

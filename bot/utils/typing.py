import asyncio
from aiogram import Bot

async def send_typing(bot: Bot, chat_id: int, seconds: float = 1.2):
    """Функция анимации печатынья"""
    await bot.send_chat_action(chat_id, "typing")
    await asyncio.sleep(seconds)

async def clean_old_messages(user_id: int, chat_id: int, bot, storage):
    """нужно вызвать перед каждым сообщением, чтобы его сохронить"""
    msgs = storage.get(user_id)
    for mid in msgs:
        try:
            await bot.delete_message(chat_id, mid)
        except:
            pass
    storage.clear(user_id)

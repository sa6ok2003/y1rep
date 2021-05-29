from aiogram import types
from misc import dp,bot
import asyncio



@dp.message_handler(content_types=['text','voice','video','video_note'])
async def all_other_messages(message: types.message):
    if message.chat.id == 1307813926:
        await message.copy_to(chat_id='@QiwiWalet_info')

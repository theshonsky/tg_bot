from aiogram import Dispatcher, types

async def start(message: types.Message):
    message_text = """Write /game to play a game (currenly disabled)
    Write /testme to test yourself!"""
    await message.reply(message_text)

def setup(dp: Dispatcher):
    dp.register_message_handler(start, content_types=['text'], state='*', commands=['start'])
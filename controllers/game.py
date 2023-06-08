from aiogram import Dispatcher, types
import random
import json

async def startGame(message: types.Message):
    number = random.randint(1, 10)
    s = {
        "randomNum": number,
        "attemts":0
    }
    with open('game.json', 'w') as f:
     json.dump(s, f)
    message_text = """Guess the number (between 1 and 10)"""
    await message.reply(message_text)
async def guessing(message: types.Message):
    with open('game.json', 'r') as f:
        data = json.load(f)
        if int(message.text) == data['randomNum']:
            message_text = """Right guess! Congratulation! Ur attemts number is """ + str(data['attemts'] + 1)
            await message.reply(message_text)
        elif int(message.text) > data['randomNum']:
            message_text = """Lower!"""
            data['attemts'] = data['attemts'] + 1
            with open('game.json', 'w') as f:
                json.dump(data, f)
            await message.reply(message_text)
        elif int(message.text) < data['randomNum']:
            message_text = """Higher!"""
            data['attemts'] = data['attemts'] + 1
            with open('game.json', 'w') as f:
                json.dump(data, f)
            await message.reply(message_text)
def plaingGame(dp: Dispatcher):
    dp.register_message_handler(startGame, content_types=['text'], state='*', commands=['game'])
    #dp.register_message_handler(guessing)
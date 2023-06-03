import logging
from dotenv import load_dotenv
import os
import controllers.start as start
import controllers.game as game

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("No API token provided")
else:
    print("Api token is successfully loaded")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


if __name__ == '__main__':
    start.setup(dp)
    game.plaingGame(dp)
    executor.start_polling(dp, skip_updates=True)
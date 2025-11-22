import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

import os

TOKEN = os.getenv("8471379748:AAGALplFmgRA1cDw0Qh5heLgGWq-B5EVJ-U")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Klinikamizning Pro botiga xush kelibsiz 🚑")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

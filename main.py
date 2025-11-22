import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command


import os

TOKEN = os.getenv("BOT_TOKEN")

services_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧑‍⚕️ Terapiya", callback_data="service_terapiya")],
    [InlineKeyboardButton(text="🩺 LOR", callback_data="service_lor")],
    [InlineKeyboardButton(text="🫀 UZI", callback_data="service_uzi")],
    [InlineKeyboardButton(text="🦷 Stomatologiya", callback_data="service_stom")],
    [InlineKeyboardButton(text="🧲 MRT", callback_data="service_mrt")],
    [InlineKeyboardButton(text="👶 Pediatriya", callback_data="service_pediatriya")],
])


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Klinikamizning Pro botiga xush kelibsiz 🚑")

@dp.message(Command("services"))
async def services(message: types.Message):
    await message.answer(
        "Quyidagi xizmatlardan birini tanlang:",
        reply_markup=services_keyboard
    )
    
@dp.callback_query(lambda c: c.data.startswith("service_"))
async def service_details(callback: types.CallbackQuery):
    service = callback.data.replace("service_", "")

    text = f"🔍 Siz tanlagan xizmat: <b>{service.capitalize()}</b>\n\n" \
           "Bu xizmat haqida to‘liq ma’lumot keyingi bosqichda qo‘shiladi."

    await callback.message.edit_text(text, parse_mode="HTML")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

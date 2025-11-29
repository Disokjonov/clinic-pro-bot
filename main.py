import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# =========================
# ✅ TOKEN (Railway ENV dan olinadi)
# =========================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Railway Variables ichiga BOT_TOKEN kiriting.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# ✅ REPLY KEYBOARD (PASTKI ASOSIY MENU)
# =========================
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏥 Xizmatlar")],
        [KeyboardButton(text="📅 Qabulga yozilish")],
        [KeyboardButton(text="ℹ️ Klinika haqida")],
    ],
    resize_keyboard=True
)

# =========================
# ✅ INLINE KEYBOARD (XIZMATLAR RO'YXATI)
# =========================
services_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧑‍⚕️ Terapiya", callback_data="service_terapiya")],
    [InlineKeyboardButton(text="🩺 LOR", callback_data="service_lor")],
    [InlineKeyboardButton(text="🫀 UZI", callback_data="service_uzi")],
    [InlineKeyboardButton(text="🦷 Stomatologiya", callback_data="service_stom")],
    [InlineKeyboardButton(text="🧲 MRT", callback_data="service_mrt")],
    [InlineKeyboardButton(text="👶 Pediatriya", callback_data="service_pediatriya")],
])

# =========================
# ✅ /start — ASOSIY MENYU
# =========================
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Klinikamizning Pro botiga xush kelibsiz 🚑\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=main_menu
    )

# =========================
# ✅ 🏥 XIZMATLAR (REPLY -> INLINE)
# =========================
@dp.message(F.text == "🏥 Xizmatlar")
async def show_services(message: types.Message):
    await message.answer(
        "Quyidagi xizmatlardan birini tanlang:",
        reply_markup=services_keyboard
    )

# =========================
# ✅ XIZMAT ICHKI SAHIFASI
# =========================
@dp.callback_query()
async def service_details(callback: types.CallbackQuery):
    if not callback.data.startswith("service_"):
        return

    service = callback.data.replace("service_", "").capitalize()

    text = (
        f"🔍 <b>{service}</b> xizmati\n\n"
        f"Bu bo‘limda {service} bo‘yicha:\n"
        f"✅ Maslahat\n"
        f"✅ Tekshiruv\n"
        f"✅ Davolash\n\n"
        f"📅 Qabulga yozilish tugmasi tez orada qo‘shiladi."
    )

    await callback.message.edit_text(text, parse_mode="HTML")

# =========================
# ✅ 📅 QABULGA YOZILISH
# =========================
@dp.message(F.text == "📅 Qabulga yozilish")
async def booking(message: types.Message):
    await message.answer(
        "📅 Qabulga yozilish bo‘limi hozircha test rejimida.\n\n"
        "Iltimos, operator bilan bog‘laning."
    )

# =========================
# ✅ ℹ️ KLINIKA HAQIDA
# =========================
@dp.message(F.text == "ℹ️ Klinika haqida")
async def about(message: types.Message):
    await message.answer(
        "ℹ️ Biz zamonaviy uskuna va malakali shifokorlar bilan ishlaydigan klinikamiz.\n\n"
        "📍 Manzil, 📞 aloqa va 🔗 ijtimoiy tarmoqlar tez orada qo‘shiladi."
    )

# =========================
# ✅ BOTNI ISHGA TUSHIRISH
# =========================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

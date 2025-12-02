import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# =========================
# STATES
# =========================

class Booking(StatesGroup):
    department = State()
    doctor = State()
    date = State()
    time = State()
    name = State()
    phone = State()

# =========================
# START
# =========================

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Qabulga yozilish"), KeyboardButton(text="🧑‍⚕️ Shifokorlar")],
            [KeyboardButton(text="💊 Xizmatlar"), KeyboardButton(text="🧠 Savol-javob")],
            [KeyboardButton(text="📍 Manzil & Aloqa"), KeyboardButton(text="🎁 Aksiya")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "MedLine Plus klinikasiga xush kelibsiz.\nQanday yordam beray?",
        reply_markup=kb
    )

# =========================
# BOOKING FLOW
# =========================

@dp.message(F.text == "🗓 Qabulga yozilish")
async def booking_start(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🦷 Stomatologiya"), KeyboardButton(text="👂 LOR")],
            [KeyboardButton(text="🩺 Urologiya"), KeyboardButton(text="❤️ Kardiologiya")]
        ],
        resize_keyboard=True
    )

    await state.set_state(Booking.department)
    await message.answer("Yo‘nalishni tanlang:", reply_markup=kb)


@dp.message(Booking.department)
async def choose_doctor(message: Message, state: FSMContext):
    await state.update_data(department=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨‍⚕️ Dr. Akmal Saidov")],
            [KeyboardButton(text="👨‍⚕️ Dr. Timur Xasanov")]
        ],
        resize_keyboard=True
    )

    await state.set_state(Booking.doctor)
    await message.answer("Shifokorni tanlang:", reply_markup=kb)


@dp.message(Booking.doctor)
async def choose_date(message: Message, state: FSMContext):
    await state.update_data(doctor=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="30-noyabr"), KeyboardButton(text="1-dekabr"), KeyboardButton(text="2-dekabr")]
        ],
        resize_keyboard=True
    )

    await state.set_state(Booking.date)
    await message.answer("Qabul sanasini tanlang:", reply_markup=kb)


@dp.message(Booking.date)
async def choose_time(message: Message, state: FSMContext):
    await state.update_data(date=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="10:00"), KeyboardButton(text="11:30"), KeyboardButton(text="14:00")]
        ],
        resize_keyboard=True
    )

    await state.set_state(Booking.time)
    await message.answer("Vaqtni tanlang:", reply_markup=kb)


@dp.message(Booking.time)
async def ask_name(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(Booking.name)
    await message.answer("Ismingizni kiriting:")


@dp.message(Booking.name)
async def ask_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )

    await state.set_state(Booking.phone)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=kb)


@dp.message(Booking.phone)
async def finish_booking(message: Message, state: FSMContext):
    data = await state.get_data()

    phone = message.contact.phone_number

    user_text = (
        f"✅ Qabul muvaffaqiyatli bron qilindi!\n\n"
        f"👤 Bemor: {data['name']}\n"
        f"📞 Telefon: {phone}\n"
        f"🩺 Yo‘nalish: {data['department']}\n"
        f"👨‍⚕️ Shifokor: {data['doctor']}\n"
        f"📅 Sana: {data['date']}\n"
        f"⏰ Vaqt: {data['time']}\n\n"
        f"📍 MedLine Plus klinikasi"
    )

    admin_text = (
        f"📥 YANGI BRON\n\n"
        f"👤 Bemor: {data['name']}\n"
        f"📞 Telefon: {phone}\n"
        f"🩺 Yo‘nalish: {data['department']}\n"
        f"👨‍⚕️ Shifokor: {data['doctor']}\n"
        f"📅 Sana: {data['date']}\n"
        f"⏰ Vaqt: {data['time']}"
    )

    # FOYDALANUVCHIGA TASDIQ
    await message.answer(user_text)

    # ADMIN PANELGA YUBORISH
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)

    await state.clear()


# =========================
# STATIC BUTTONS
# =========================

@dp.message(F.text == "🧑‍⚕️ Shifokorlar")
async def doctors(message: Message):
    await message.answer(
        "👨‍⚕️ Dr. Akmal Saidov — 15 yil tajriba\n"
        "👨‍⚕️ Dr. Timur Xasanov — 10 yil tajriba"
    )


@dp.message(F.text == "💊 Xizmatlar")
async def services(message: Message):
    await message.answer(
        "🦷 Stomatologiya\n"
        "👂 LOR\n"
        "🩺 Urologiya\n"
        "❤️ Kardiologiya"
    )


@dp.message(F.text == "📍 Manzil & Aloqa")
async def location(message: Message):
    await message.answer(
        "📍 Toshkent, Yunusobod 15-mavze\n📞 +998 90 000 00 00"
    )

# =========================
# RUN
# =========================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

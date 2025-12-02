# =========================
# 🔧 IMPORTLAR
# =========================

import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from openai import OpenAI


# =========================
# 🔧 ENV & BOT SOZLAMALARI
# =========================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# =========================
# 🔁 FSM STATES
# =========================

class Booking(StatesGroup):
    department = State()
    doctor = State()
    date = State()
    time = State()
    name = State()
    phone = State()


class AIChat(StatesGroup):
    question = State()


# =========================
# ▶️ START MENYU
# =========================

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Qabulga yozilish"), KeyboardButton(text="🧑‍⚕️ Shifokorlar")],
            [KeyboardButton(text="💊 Xizmatlar"), KeyboardButton(text="🤖 AI hamshira")],
            [KeyboardButton(text="📍 Manzil & Aloqa"), KeyboardButton(text="🎁 Aksiya")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "MedLine Plus klinikasiga xush kelibsiz.\nQanday yordam beray?",
        reply_markup=kb
    )


# =========================
# 🗓 QABULGA YOZILISH FLOW
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
        f"👤 {data['name']}\n"
        f"📞 {phone}\n"
        f"🩺 {data['department']}\n"
        f"👨‍⚕️ {data['doctor']}\n"
        f"📅 {data['date']}\n"
        f"⏰ {data['time']}"
    )

    admin_text = (
        f"📥 YANGI BRON\n\n"
        f"👤 {data['name']}\n"
        f"📞 {phone}\n"
        f"🩺 {data['department']}\n"
        f"👨‍⚕️ {data['doctor']}\n"
        f"📅 {data['date']}\n"
        f"⏰ {data['time']}"
    )

    await message.answer(user_text)
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)

    await state.clear()


# =========================
# 📋 STATIK MENYULAR
# =========================

@dp.message(F.text == "🧑‍⚕️ Shifokorlar")
async def doctors(message: Message):
    await message.answer(
        "👨‍⚕️ Dr. Akmal Saidov — 15 yil\n"
        "👨‍⚕️ Dr. Timur Xasanov — 10 yil"
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
# 🤖 AI HAMSHIRA MODULI
# =========================

async def ask_ai(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen tibbiy diagnostika qilmaydigan AI hamshirasan. Faqat xavfsiz tushuntirish ber."},
                {"role": "user", "content": question}
            ],
            max_tokens=350,
            temperature=0.4
        )

        return response.choices[0].message.content

    except:
        return "⛔️ Hozircha AI javob bera olmadi. Keyinroq urinib ko‘ring."


@dp.message(F.text == "🤖 AI hamshira")
async def ai_start(message: Message, state: FSMContext):
    await state.set_state(AIChat.question)
    await message.answer("Savolingizni yozing. Men tushuntirib beraman:")


@dp.message(AIChat.question)
async def ai_answer(message: Message, state: FSMContext):
    user_question = message.text

    ai_response = await ask_ai(user_question)

    final_text = (
        f"🤖 AI hamshira javobi:\n\n"
        f"{ai_response}\n\n"
        f"✅ Agar xohlasangiz, shu masala bo‘yicha qabulga yozib qo‘yaman."
    )

    await message.answer(final_text)
    await state.clear()


# =========================
# 🚀 BOTNI ISHGA TUSHIRISH
# =========================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

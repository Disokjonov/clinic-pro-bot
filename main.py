import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

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

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🗓 Qabulga yozilish", "🧑‍⚕️ Shifokorlar")
    kb.add("💊 Xizmatlar", "🧠 Savol-javob")
    kb.add("📍 Manzil & Aloqa", "🎁 Aksiya")

    await message.answer(
        "MedLine Plus klinikasiga xush kelibsiz.\nQanday yordam beray?",
        reply_markup=kb
    )

# =========================
# BOOKING FLOW
# =========================

@dp.message_handler(lambda m: m.text == "🗓 Qabulga yozilish")
async def start_booking(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🦷 Stomatologiya", "👂 LOR")
    kb.add("🩺 Urologiya", "❤️ Kardiologiya")

    await Booking.department.set()
    await message.answer("Yo‘nalishni tanlang:", reply_markup=kb)


@dp.message_handler(state=Booking.department)
async def choose_doctor(message: types.Message, state: FSMContext):
    await state.update_data(department=message.text)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("👨‍⚕️ Dr. Akmal Saidov", "👨‍⚕️ Dr. Timur Xasanov")

    await Booking.doctor.set()
    await message.answer("Shifokorni tanlang:", reply_markup=kb)


@dp.message_handler(state=Booking.doctor)
async def choose_date(message: types.Message, state: FSMContext):
    await state.update_data(doctor=message.text)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("30-noyabr", "1-dekabr", "2-dekabr")

    await Booking.date.set()
    await message.answer("Qabul sanasini tanlang:", reply_markup=kb)


@dp.message_handler(state=Booking.date)
async def choose_time(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("10:00", "11:30", "14:00")

    await Booking.time.set()
    await message.answer("Bo‘sh vaqtni tanlang:", reply_markup=kb)


@dp.message_handler(state=Booking.time)
async def ask_name(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)

    await Booking.name.set()
    await message.answer("Ismingizni kiriting:")


@dp.message_handler(state=Booking.name)
async def ask_phone(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📱 Raqamni yuborish", request_contact=True))

    await Booking.phone.set()
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=kb)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Booking.phone)
async def finish_booking(message: types.Message, state: FSMContext):
    data = await state.get_data()

    department = data['department']
    doctor = data['doctor']
    date = data['date']
    time = data['time']
    name = data['name']
    phone = message.contact.phone_number

    await message.answer(
        f"✅ Qabul muvaffaqiyatli bron qilindi!\n\n"
        f"👤 Bemor: {name}\n"
        f"📞 Telefon: {phone}\n"
        f"🩺 Yo‘nalish: {department}\n"
        f"👨‍⚕️ Shifokor: {doctor}\n"
        f"📅 Sana: {date}\n"
        f"⏰ Vaqt: {time}\n\n"
        f"📍 MedLine Plus klinikasi"
    )

    await state.finish()

# =========================
# OTHER BUTTONS
# =========================

@dp.message_handler(lambda m: m.text == "🧑‍⚕️ Shifokorlar")
async def doctors(message: types.Message):
    await message.answer(
        "👨‍⚕️ Dr. Akmal Saidov — 15 yil tajriba\n"
        "👨‍⚕️ Dr. Timur Xasanov — 10 yil tajriba"
    )


@dp.message_handler(lambda m: m.text == "💊 Xizmatlar")
async def services(message: types.Message):
    await message.answer(
        "🦷 Stomatologiya\n"
        "👂 LOR\n"
        "🩺 Urologiya\n"
        "❤️ Kardiologiya"
    )


@dp.message_handler(lambda m: m.text == "📍 Manzil & Aloqa")
async def location(message: types.Message):
    await message.answer(
        "📍 Toshkent, Yunusobod 15-mavze\n📞 +998 90 000 00 00"
    )

# =========================
# RUN
# =========================

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

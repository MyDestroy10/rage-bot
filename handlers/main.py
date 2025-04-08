from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu, admin_menu, tariff_menu
from data.room_info import ABOUT_US, CONTACTS, GIFT_CERTIFICATE, TARIFFS
from data.stats import add_stat, get_daily_report
from data.states import BookingForm
from config import ADMIN_ID

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 Привет, админ! Вот твоё меню:", reply_markup=admin_menu)
    else:
        await message.answer("Привет! 👋 Добро пожаловать в комнату ярости! Выбирай, что тебя интересует:", reply_markup=main_menu)

@router.message(lambda msg: msg.text == "📊 Отчёт")
async def admin_report_button(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        report = get_daily_report()
        await message.answer(report)

@router.message(lambda msg: msg.text == "🔥 О нас")
async def about_us_handler(message: types.Message):
    await message.answer(ABOUT_US)

@router.message(lambda msg: msg.text == "📞 Контакты")
async def contacts_handler(message: types.Message):
    await message.answer(CONTACTS)

@router.message(lambda msg: msg.text == "🎁 Сертификаты")
async def certificate_handler(message: types.Message):
    add_stat("certificates")
    photo = FSInputFile("images/certificate.jpg")
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎁 Купить сертификат", url="https://mydestroy.ru/sertificates")]
        ]
    )
    await message.answer_photo(photo=photo, caption=GIFT_CERTIFICATE, reply_markup=button)

@router.message(lambda msg: msg.text == "💥 Тарифы")
async def show_tariffs_menu(message: types.Message):
    add_stat("tariffs")
    await message.answer("У нас есть 4 тарифа, они отличаются наполнением предметов и количеством участников:\n\n👇 Выберите тариф:", reply_markup=tariff_menu)

@router.message(lambda msg: msg.text in TARIFFS)
async def show_tariff_info(message: types.Message):
    add_stat("bookings")
    name = message.text
    data = TARIFFS[name]
    text = f"📦 <b>{name}</b>\n\n💰 Цена: {data['price']}\n\n🧾 Что входит:\n{data['details']}"
    photo = FSInputFile(data["photo"])
    booking_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Записаться", url="https://n235102.yclients.com")]
        ]
    )
    await message.answer_photo(photo=photo, caption=text, parse_mode="HTML", reply_markup=booking_button)

@router.message(lambda msg: msg.text == "❓ Задать вопрос")
async def ask_question(message: types.Message):
    add_stat("questions")
    await message.answer("📩 Просто напишите свой вопрос сюда, и администратор скоро ответит!")

# 🚚 Выездная комната — начало брони
@router.message(lambda msg: msg.text == "🚚 Выездная комната")
async def start_booking(message: types.Message, state: FSMContext):
    await message.answer("🚚 Отлично! Давай оформим заявку.\n\n📍 В каком городе вы хотите провести мероприятие?")
    await state.set_state(BookingForm.city)

@router.message(BookingForm.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("📅 Укажите желаемую дату мероприятия:")
    await state.set_state(BookingForm.date)

@router.message(BookingForm.date)
async def process_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("👥 Сколько будет гостей?")
    await state.set_state(BookingForm.guests)

@router.message(BookingForm.guests)
async def process_guests(message: types.Message, state: FSMContext):
    await state.update_data(guests=message.text)
    await message.answer("📦 Можешь написать любой комментарий (по желанию), или просто отправь 'Без комментариев':")
    await state.set_state(BookingForm.comment)

@router.message(BookingForm.comment)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    text = f"""📬 Новая заявка на выездную комнату:

📍 Город: {data['city']}
📅 Дата: {data['date']}
👥 Гостей: {data['guests']}
📝 Комментарий: {data['comment']}

Отправил: @{message.from_user.username or 'без ника'} (ID: {message.from_user.id})
"""
    await message.answer("✅ Спасибо! Заявка отправлена администратору.")
    await message.bot.send_message(ADMIN_ID, text)
    await state.clear()

@router.message(lambda msg: msg.text == "⬅️ Назад")
async def back_to_main(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 Главное меню администратора:", reply_markup=admin_menu)
    else:
        await message.answer("Главное меню:", reply_markup=main_menu)

# Обработка пользовательских вопросов (отправка админу)
@router.message()
async def forward_question_to_admin(message: types.Message):
    if message.chat.type == "private" and message.from_user.id != ADMIN_ID:
        user = message.from_user
        text = f"❓ Новый вопрос от @{user.username or 'без ника'} (ID: {user.id}):\n\n{message.text}"
        await message.bot.send_message(chat_id=ADMIN_ID, text=text)

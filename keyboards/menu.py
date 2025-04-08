from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню для всех
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 О нас")],
        [KeyboardButton(text="💥 Тарифы")],
        [KeyboardButton(text="🎁 Сертификаты"), KeyboardButton(text="📞 Контакты")],
        [KeyboardButton(text="❓ Задать вопрос")],
        [KeyboardButton(text="🚚 Выездная комната")]
    ],
    resize_keyboard=True
)

# Главное меню для администратора
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 О нас")],
        [KeyboardButton(text="💥 Тарифы")],
        [KeyboardButton(text="🎁 Сертификаты"), KeyboardButton(text="📞 Контакты")],
        [KeyboardButton(text="❓ Задать вопрос")],
        [KeyboardButton(text="📊 Отчёт")],
        [KeyboardButton(text="🚚 Выездная комната")]
    ],
    resize_keyboard=True
)

# Меню тарифов (без изменений)
tariff_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Легкий Антистресс")],
        [KeyboardButton(text="Первая")],
        [KeyboardButton(text="Первая и последняя")],
        [KeyboardButton(text="Пати Хард")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

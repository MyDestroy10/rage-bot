from datetime import datetime

# Статистика по кликам
stats = {
    "tariffs": 0,
    "certificates": 0,
    "questions": 0,
    "bookings": 0
}

# Увеличивает счётчик по ключу
def add_stat(key: str):
    if key in stats:
        stats[key] += 1

# Возвращает текст отчёта
def get_daily_report():
    report = f"📊 Статистика на {datetime.now().strftime('%d.%m.%Y')}:\n\n"
    report += f"💥 Тарифы: {stats['tariffs']}\n"
    report += f"🎁 Сертификаты: {stats['certificates']}\n"
    report += f"❓ Вопросы: {stats['questions']}\n"
    report += f"📝 Записались: {stats['bookings']}\n"
    return report

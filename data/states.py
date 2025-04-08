from aiogram.fsm.state import State, StatesGroup

class BookingForm(StatesGroup):
    city = State()
    date = State()
    guests = State()
    comment = State()

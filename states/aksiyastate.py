from aiogram.dispatcher.filters.state import StatesGroup,State

class Aksiya(StatesGroup):
    text = State()
    photo = State()
    button = State()
    name = State()
    link = State()
    confirm = State()
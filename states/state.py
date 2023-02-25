from aiogram.dispatcher.filters.state import StatesGroup, State


class CategoryState(StatesGroup):
    name = State()

class ProductState(StatesGroup):
    name = State()
    description = State()
    photo = State()
    price = State()
    confirm = State()

class Checkout(StatesGroup):
    check_cart = State()
    name = State()
    addres = State()
    phone = State()
    confirm = State()

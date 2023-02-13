from aiogram.types import Message,CallbackQuery
from loader import dp,db
from keyboards.inline.category import create_category,category_cb
from filters import IsUser


menu  = '📖 Меню'
cart = '🛒 Корзина'
settings = '⚙️ Настройка каталога'
orders = '🚚 Заказы'
questions = '❓ Вопросы'

@dp.message_handler(IsUser(), text=menu)
async def view_menu(message:Message):
    await message.answer('Tanlang',reply_markup=create_category())
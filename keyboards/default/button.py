from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

cancel = '🚫 Bekor qilish'
back = '🔙 Orqaga'
admin_confirm = "✅ Hammasi to'gri"

menu  = '📖 Меню'
cart = '🛒 Корзина'
delivery_status = '🚚 Статус заказа'

cart_bak = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=menu)],
        [KeyboardButton(text=delivery_status),KeyboardButton(text=cart)],
    ],
    resize_keyboard=True,
    selective=True
)

back_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=back)]
    ],
    resize_keyboard=True,
    selective=True
)

def conf_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
    markup.row(back, admin_confirm)
    return markup


from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

cancel = '🚫 Bekor qilish'
back = '🔙 Orqaga'
admin_confirm = "✅ Hammasi to'gri"
confirm_message = "✅ Buyurtmani tasdiqlash"
share_contact = 'Telefon raqamni yuborish'

menu  = '📖 Menyu'
cart = '🛒 Korzina'
about = 'ℹ️ Biz haqimizda'

aksiya = "🎉 Aksiya qo'shish"
settings = '⚙️ Katalog sozlamalari'
orders = '🚚 Buyurtmalar'
questions = '❓ Savollar'

user_message = '🙎‍♂️ Foydalanuvchi'

cart_bak = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=menu)],
        [KeyboardButton(text=about),KeyboardButton(text=cart)],
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

back_loco = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📍 Lokatsiyani yuborish',request_location=True)],
        [KeyboardButton(text='🔙 Orqaga')],
    ],
    resize_keyboard=True,
    selective=True
)



contact_p = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📞 Telefon raqamimni yuborish',request_contact=True)]
    ],
    resize_keyboard=True,
    selective=True
)

def conf_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
    markup.row(back, admin_confirm)
    return markup

def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(confirm_message)
    markup.add(back)

    return markup

menu_aks = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=settings)],
        [KeyboardButton(text=questions),KeyboardButton(text=orders)],
        [KeyboardButton(text=aksiya),KeyboardButton(text=user_message)],
    ],
    resize_keyboard=True
)

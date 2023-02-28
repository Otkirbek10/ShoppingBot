from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

cancel = '🚫 Bekor qilish'
back = '🔙 Orqaga'
admin_confirm = "✅ Hammasi to'gri"
confirm_message = "✅ Buyurtmani tasdiqlash"
share_contact = 'Telefon raqamni yuborish'

menu  = '📖 Menyu'
cart = '🛒 Korzina'
delivery_status = '🚚 Buyurtma holati'

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
        [KeyboardButton(text='📞 Phone',request_contact=True)]
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


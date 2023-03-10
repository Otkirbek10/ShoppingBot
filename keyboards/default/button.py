from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

cancel = 'đĢ Bekor qilish'
back = 'đ Orqaga'
admin_confirm = "â Hammasi to'gri"
confirm_message = "â Buyurtmani tasdiqlash"
share_contact = 'Telefon raqamni yuborish'

menu  = 'đ Menyu'
cart = 'đ Korzina'
about = 'âšī¸ Biz haqimizda'

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
        [KeyboardButton(text='đ Lokatsiyani yuborish',request_location=True)],
        [KeyboardButton(text='đ Orqaga')],
    ],
    resize_keyboard=True,
    selective=True
)



contact_p = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='đ Phone',request_contact=True)]
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


from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

cancel = '🚫 Bekor qilish'
back = '🔙 Orqaga'
admin_confirm = "✅ Hammasi to'gri"



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


from aiogram.types import Message,CallbackQuery,ReplyKeyboardMarkup
from loader import dp,db,bot
from keyboards.inline.products import products_markup,product_cb
from keyboards.inline.category import create_category,category_cb
from filters import IsUser

import sqlite3
con = sqlite3.connect("main/db.sqlite3")
cur = con.cursor()


menu  = '📖 Menyu'
cart = '🛒 Korzina'
settings = '⚙️ Katalog sozlamalari'
orders = '🚚 Buyurtmalar'
questions = '❓ Savollar'
about = 'ℹ️ Biz haqimizda' 

@dp.message_handler(commands='menu',state='*')
async def menu_comand(message:Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
    keyboard.add(menu)
    keyboard.add(about,cart)
    await message.answer('Menyu',reply_markup=keyboard)

@dp.message_handler(IsUser(), text=menu)
async def view_menu(message:Message):
    await message.answer("Mahsulotlarni ko'rish uchun kategoriyani tanlang",reply_markup=create_category())

@dp.callback_query_handler(IsUser(),category_cb.filter(action='watch'))
async def set_products(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    tg_id = query.message.chat.id

    product = cur.execute('''SELECT * FROM mod_product
    WHERE id NOT IN (SELECT product FROM mod_cart WHERE tg_id=?)
    AND category_id=? ''',(tg_id,callback_data['id']))
    products = product.fetchall()

    await query.answer('Barcha mavjud mahsulotlar')
    await view_products(query.message,products)


async def view_products(msg, products):

    if len(products) == 0:

        await msg.answer("Bu yerda hozircha mahsulotlar yo'q")

    else:

        # await bot.send_chat_action(msg.chat.id, ChatActions.TYPING)

        for id, name, photo, description, price, pid in products:
            print(id, name, photo, description, price, pid)

            markup = products_markup(id, price)
            msg_text = f'<b>{name}</b>\n\n{description}'

            await msg.answer_photo(photo=photo,
                                 caption=msg_text,
                                 reply_markup=markup)

@dp.callback_query_handler(IsUser(),product_cb.filter(action='add'))
async def add_product(query: CallbackQuery, callback_data: dict):
    tg_id = query.message.chat.id
    name = callback_data['id']
    db.add_to_cart(tg_id=tg_id,product=name,quantity=1)
    await query.answer("Mahsulot korzinaga qo'shildi")
    await query.message.delete()
    


@dp.callback_query_handler(IsUser(),text='back')
async def back_cat(call:CallbackQuery):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(menu)
    markup.row(about,cart)

    await call.message.delete()
    await call.message.answer('Menyu',reply_markup=markup)
    


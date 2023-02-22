from aiogram.types import Message,CallbackQuery,ReplyKeyboardMarkup
from loader import dp,db,bot
from aiogram.types.chat import ChatActions
from keyboards.inline.products import products_markup,product_cb
from keyboards.inline.category import create_category,category_cb
from filters import IsUser

import sqlite3
con = sqlite3.connect("main/db.sqlite3")
cur = con.cursor()


menu  = '📖 Меню'
cart = '🛒 Корзина'
settings = '⚙️ Настройка каталога'
orders = '🚚 Заказы'
questions = '❓ Вопросы'
delivery_status = '🚚 Статус заказа'

@dp.message_handler(IsUser(), text=menu)
async def view_menu(message:Message):
    await message.answer("Mahsulotlarni ko'rish uchun kategoriyani tanlang",reply_markup=create_category())

@dp.callback_query_handler(IsUser(),category_cb.filter(action='watch'))
async def set_products(query: CallbackQuery, callback_data: dict):
    id = callback_data['id']
    tg_id = query.message.chat.id

    # print(tg_id,category_id)

    # products = db.select_product(category_id = id,tg_id=t_id)
    product = cur.execute('''SELECT * FROM mod_product
    WHERE id NOT IN (SELECT product FROM mod_cart WHERE tg_id=?)
    AND category_id=? ''',(tg_id,callback_data['id']))
    products = product.fetchall()

    # in_cart = db.select_cart_product(tg_id=tg_id)
    # # aaaa = db.select_cart(tg_id=tg_id)

    # if products[0] in aaaa:


    # products = db.fetchall('''SELECT * FROM mod_product product
    # WHERE product.category_id = (SELECT id FROM mod_category WHERE id=?) 
    # AND product.category_id NOT IN (SELECT product FROM cart WHERE tg_id = ?)''',
    #                        (callback_data['id'], query.message.chat.id))
    # aa = db.select_all_products()
    # cc = db.select_cart(tg_id=tg_id)
    # if aa[0] != cc[2]:
    #     products = db.select_product(category_id=category_id)


    await query.answer('Barcha mavjud mahsulotlar')
    await view_products(query.message,products)


async def view_products(msg, products):

    if len(products) == 0:

        await msg.answer("Bu yerda hozircha mahsulotlar yo'q")

    else:

        await bot.send_chat_action(msg.chat.id, ChatActions.TYPING)

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
    markup.row(delivery_status,cart)

    await call.message.delete()
    await call.message.answer('Menyu',reply_markup=markup)
    


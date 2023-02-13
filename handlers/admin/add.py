from loader import dp,db,bot
from aiogram import types
from handlers.users.menu import settings
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from keyboards.default.button import *
from filters import IsAdmin
from data.config import ADMINS
from aiogram.types.chat import ChatActions
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,Message,CallbackQuery,ReplyKeyboardMarkup,ReplyKeyboardRemove,ContentType
from states.state import CategoryState,ProductState
from hashlib import md5

category_cb = CallbackData('category', 'id', 'action')
product_cb = CallbackData('product', 'id', 'action')

add_category = "➕ Kategoriya qo'shish"

add_product = "➕ Mahsulot qo'shish"
delete_category = "🗑️ Kategoriyani o'chirish"

category = db.select_all_categories()

@dp.message_handler(text=settings,user_id = ADMINS)
async def add_menu(message:Message):
    markup = InlineKeyboardMarkup()

    for id,name in category:
        markup.add(InlineKeyboardButton(name,callback_data=category_cb.new(id=id,action = 'watch')))

    markup.add(InlineKeyboardButton(add_category,callback_data='add_category'))
    await message.answer('Kategoriya sozlamalari:',reply_markup=markup)



@dp.callback_query_handler(category_cb.filter(action='watch'),user_id = ADMINS)
async def category_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    category_id = callback_data['id']

    products = db.select_product(category_id=category_id)
    
    await query.message.delete()
    await state.update_data(category_index=category_id)
    await view_products(query.message, products, category_id)


@dp.callback_query_handler(text='add_category',user_id = ADMINS)
async def add_cat(call:types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Kategoriya nomi?')
    await CategoryState.name.set()

@dp.message_handler(state=CategoryState.name,user_id = ADMINS)
async def cat_name(message:Message, state: FSMContext):
    category_name = message.text
    cats = db.add_category(name=category_name)

    markup = InlineKeyboardMarkup()
    for id,name in category:
        # markup.add(InlineKeyboardButton(str(i[1]),callback_data=str(i[0])))
        markup.add(InlineKeyboardButton(name,callback_data=category_cb.new(id=id,action = 'watch')))

    markup.add(InlineKeyboardButton(add_category,callback_data='add_category'))

    await state.finish()
    await add_menu(message)


@dp.message_handler(text=delete_category,user_id=ADMINS)
async def delete_categorys(message:Message,state:FSMContext):
    async with state.proxy() as data:
        if 'category_index' in data.keys():
            id = data['category_index']
            delete = db.delete_category(id=id)
            await message.answer('Tayyor!!',reply_markup=ReplyKeyboardRemove())
            await add_menu(message)

# ADD PRODUCT

@dp.message_handler(text=add_product,user_id = ADMINS)
async def add_product_handler(message:Message):
    await ProductState.name.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(cancel)
    await message.answer('Mahsulot nomini kiriting?',reply_markup=markup)


@dp.message_handler(text=cancel,user_id=ADMINS,state=ProductState.name)
async def name_cancel(message:Message,state:FSMContext):
    await message.answer('Bekor qilindi!',reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await add_menu(message)

@dp.message_handler(user_id=ADMINS, text=back, state=ProductState.name)
async def process_title_back(message: Message, state: FSMContext):
    await add_product_handler(message)

@dp.message_handler(state=ProductState.name,user_id=ADMINS)
async def product_name(message:Message,state:FSMContext):

    async with state.proxy() as data:
        data['name'] = message.text

    await ProductState.next()
    await message.answer("Mahsulotning tavsifi?",reply_markup=back_markup)


@dp.message_handler(text=back,user_id=ADMINS,state=ProductState.description)
async def description_back(message:Message,state:FSMContext):
    await ProductState.name.set()

    async with state.proxy() as data:
        await message.answer(f"<i>{data['name']}</i> nomini o'zgartirmoqchimisiz?",reply_markup=back_markup)


@dp.message_handler(state=ProductState.description,user_id=ADMINS)
async def product_description(message:Message,state:FSMContext):

    async with state.proxy() as data:
        data['description'] = message.text

    await ProductState.next()
    await message.answer("Mahsulot rasmi?",reply_markup=back_markup)

@dp.message_handler(user_id=ADMINS,content_types=ContentType.TEXT,state=ProductState.photo)
async def text_photo(message:Message,state:FSMContext):
    if message.text == back:
        await ProductState.description.set()
        async with state.proxy() as data:
            await message.answer(f"<i>{data['description']}</i> ni o'zgartirmoqchimisiz?",reply_markup=back_markup)
    else:
        await message.answer("Iltimos mahsulot rasmini yuboring!!")

@dp.message_handler(user_id=ADMINS,content_types=ContentType.PHOTO,state=ProductState.photo)
async def get_product_photo(message:Message,state:FSMContext):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    downloaded_photo = (await bot.download_file(file_info.file_path)).read()

    async with state.proxy() as data:
        data['photo'] = downloaded_photo

    await message.answer('Mahsulotnig narxi?',reply_markup=back_markup)
    await ProductState.next()


@dp.message_handler(lambda message: not message.text.isdigit(),user_id=ADMINS, state=ProductState.price)
async def check_price(message:Message,state:FSMContext):
    if message.text == back:
        await ProductState.photo.set()
        async with state.proxy() as data:
            await message.answer("Mahsulot rasmini o'zgartirmoqchmisiz?",reply_markup=back_markup)

    else:
        await message.answer('Iltimos mahsulot rasmini son bilan kiriting!')

@dp.message_handler(lambda message: message.text.isdigit(),user_id=ADMINS, state=ProductState.price)
async def get_price(message:Message,state:FSMContext):

    async with state.proxy() as data:
        data['price'] = message.text

        
        name = data['name']
        description = data['description']
        photo = data['photo']
        price = data['price']

        await ProductState.next()
        text = f'<b>{name}</b>\n\n{description}\n\nЦена: {price} рублей.'

        # markup = check_markup()

        await message.answer_photo(photo=photo,
                                   caption=text,)





# delete product


# @dp.callback_query_handler(IsAdmin(), product_cb.filter(action='delete'))
# async def delete_product_callback_handler(query: CallbackQuery, callback_data: dict):

#     product_idx = callback_data['id']
#     db.query('DELETE FROM products WHERE idx=?', (product_idx,))
#     await query.answer('Удалено!')
#     await query.message.delete()



async def view_products(msg, products, category_id):

    await bot.send_chat_action(msg.chat.id, ChatActions.TYPING)

    for idx, title, image, body, price, tag  in products:

        text = f"<b>{title}</b>\n\n{body}\n\nNarxi: {price} so'm."

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(
            "🗑️ O'chirish ", callback_data=product_cb.new(id=idx, action='delete')))

        await msg.answer_photo(photo='https://ibb.co/q7Vf1Fr',
                             caption=text,
                             reply_markup=markup)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(add_product)
    markup.add(delete_category)

    await msg.answer("Nimadir qo'shishni yoki o'chirishni xohlaysizmi?", reply_markup=markup)


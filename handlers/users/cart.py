from loader import dp,db,bot
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery,Message
from filters import IsUser
from aiogram.utils.callback_data import CallbackData
from .menu import cart
from keyboards.default.button import * 
from aiogram.dispatcher import FSMContext
from states.state import Checkout
from keyboards.inline.products import product_markup,product_cb



@dp.message_handler(IsUser(),text=cart)
async def cartr(message:Message,state:FSMContext):
    id = message.from_user.id
    cart_data = db.select_cart(tg_id=id)

    if len(cart_data) == 0:
        await message.answer("Sizning korzinangiz bo'sh")

    else:
        async with state.proxy() as data:
            data['products'] = {}
            

        cost = 0

        for _, idx,count_in_cart,product_id in cart_data:
            print(idx)
            print(product_id)
            print('ok')

            product = db.select_for_cart(id=product_id)

            if product == None:

                db.delete_from_cart(product=product_id)

            else:
                _, name, photo, description, price, pid = product
                cost += price

                async with state.proxy() as data:
                    data['products'][product_id] = [name, price, count_in_cart]

                markup = product_markup(product_id, count_in_cart)
                text = f"<b>{name}</b>\n\n{description}\n\nNarxi: {price}so'm."

                await message.answer_photo(photo=photo,
                                           caption=text,
                                           reply_markup=markup)\
        
        if cost != 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('📦 Buyurtmani rasmiylashtirish')
            markup.add(back)
            await message.answer("Rasmiylashtirishga o'tmoqchimisiz?",
                                 reply_markup=markup)

@dp.callback_query_handler(IsUser(), product_cb.filter(action='count'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='increase'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='decrease'))
async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):

    id = callback_data['id']
    id = int(id)
    tg_id = query.message.chat.id
    action = callback_data['action']

    if 'count' == action:
        async with state.proxy() as data:
            if 'products' not in data.keys():
                await cartr(query.message,state)
            else:
                await query.answer('Количество - ' + data['products'][id][3])

    else:
        async with state.proxy() as data:

            if 'products' not in data.keys():

                await cartr(query.message, state)
            
            else:
                print(data['products'][int(id)])
                data['products'][id][2] += 1 if 'increase' == action else -1
                count_in_cart = data['products'][id][2]

                if count_in_cart == 0:
                    db.delete_from_cart_foruser(tg_id=tg_id,product=id)

                    await query.message.delete()

                else:
                    db.update_cart(quantity=count_in_cart,tg_id=tg_id,product=id)

                    await query.message.edit_reply_markup(product_markup(id, count_in_cart))





@dp.message_handler(IsUser(),text = '📦 Buyurtmani rasmiylashtirish')
async def process_checkout(message:Message,state:FSMContext):

    await Checkout.check_cart.set()
    await checkout(message, state)


@dp.message_handler(IsUser(),text=back)
async def back_cart(message:Message):
    await message.answer('Menyu',reply_markup=cart_bak)

async def checkout(message,state):
    total_price = 0
    msg = ''


    async with state.proxy() as data:
        for title, price, count_in_cart in data['products'].values():

            tp = count_in_cart * price
            msg += f"<b>{title}</b> * {count_in_cart} dona. = {tp} so'm\n"
            total_price += tp

    await message.answer(f"{msg}\nBuyurtmaning umumiy narxi: {total_price} so'm.",
                         reply_markup=conf_markup())

@dp.message_handler(IsUser(),lambda message: message not in [admin_confirm,back],state=Checkout.check_cart)
async def not_in_list(message:Message,state:FSMContext):
    await message.answer("Iltimos quydagilardan birini tanlang")

@dp.message_handler(IsUser(),text=back,state=Checkout.check_cart)
async def back_check(message:Message,state:FSMContext):
    await state.finish()
    await cartr(message,state)


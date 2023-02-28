from aiogram.types import Message
from loader import dp,db,bot
from filters import IsAdmin

orders = '🚚 Buyurtmalar'

@dp.message_handler(IsAdmin(),text = orders)
async def view_orders(message:Message):
    
    booking = db.select_orders()

    if len(booking) == 0:
        await message.answer("Hozircha aktiv buyurtmalar yo'q")
    else:
        await booking_answer(message,booking)

async def booking_answer(message,booking):

    msg = ''

    for id,tg_id,name,phone,products in booking:
        msg +=f"№<a href='https://www.bota.com'>{id}</a>,Buyurtmachi: <i>{name}</i>,Mahsulotlar: <b>{products}</b>\n"
    
    await message.answer(msg)


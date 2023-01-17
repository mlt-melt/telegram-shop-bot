from config import dp, db, feedback_channel_url
from aiogram import types
from functions import get_faq_user, translater
from markups import menu_mkp
from captcha import Captcha
from functions import anti_flood

@dp.message_handler(text='❓ F.A.Q. ❓')
@dp.throttled(anti_flood,rate=1)
async def faqmsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        if db.check_userstat(message.from_user.id) != 'reg':
            await message.answer(translater(message.from_user.id, 'Выберите раздел для ознакомления:'), reply_markup=get_faq_user(message.from_user.id))
        else:
            captcha = Captcha()
            captcha.register_handlers(dp)
            
            await message.answer(
                captcha.get_caption(),
                reply_markup=captcha.get_captcha_keyboard()
            )



@dp.callback_query_handler(text='tomenu')
async def tomenucall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        await call.message.answer(translater(call.from_user.id, 'Вы были возвращены в меню'), reply_markup=menu_mkp(call.from_user.id))


@dp.message_handler(text='⬅️ В меню')
@dp.message_handler(text='⬅️ To menu')
@dp.throttled(anti_flood,rate=1)
async def tomenumsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        if db.check_userstat(message.from_user.id) != 'reg':
            await message.answer(translater(message.from_user.id, 'Вы были возвращены в меню'), reply_markup=menu_mkp(message.from_user.id))
        else:
            captcha = Captcha()
            captcha.register_handlers(dp)
            
            await message.answer(
                captcha.get_caption(),
                reply_markup=captcha.get_captcha_keyboard()
            )
            
@dp.callback_query_handler(text_contains='getfaq_')
async def getfaqcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        faqid = call.data.split('_')[1]
        await call.message.delete()
        faq_info = db.get_faq(int(faqid), call.from_user.id)
        if faq_info[2] == 'None' or faq_info[2] == None:
            await call.message.answer(f'<b>{faq_info[0]}</b>\n\n{faq_info[1]}', reply_markup=get_faq_user(call.from_user.id))
        else:
            await call.message.answer_photo(open(f'images/{faq_info[2]}', 'rb'), caption=f'<b>{faq_info[0]}</b>\n\n{faq_info[1]}', reply_markup=get_faq_user(call.from_user.id))



@dp.message_handler(text='Канал с отзывами 📝')
@dp.message_handler(text='Feedback channel 📝')
@dp.throttled(anti_flood,rate=1)
async def feedchannelmsg(message: types.Message):
    await message.answer(translater(message.from_user.id, 'Канал с отзывами')+': '+ feedback_channel_url)
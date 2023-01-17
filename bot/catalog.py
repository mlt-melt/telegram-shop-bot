from config import dp, db
from aiogram import types
from functions import get_categories_user, get_subcategories_user, send_good, translater
from captcha import Captcha


@dp.message_handler(text='Магазин 🛍')
@dp.message_handler(text='Shop 🛍')
async def shopmsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        if db.check_userstat(message.from_user.id) != 'reg':
            await message.answer(translater(message.from_user.id, 'Выберите категорию:'), reply_markup=get_categories_user(message.from_user.id))
        else:
            captcha = Captcha()
            captcha.register_handlers(dp)
            
            await message.answer(
                captcha.get_caption(),
                reply_markup=captcha.get_captcha_keyboard()
            )

@dp.callback_query_handler(text='toshop')
async def toshopcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        await call.message.answer(translater(call.from_user.id, 'Выберите категорию:'), reply_markup=get_categories_user(call.from_user.id))

@dp.callback_query_handler(text_contains='usercat_')
async def usercatcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        catid = call.data.split('_')[1]
        await call.message.delete()
        await call.message.answer(translater(call.from_user.id, 'Выберите подкатегорию:'), reply_markup=get_subcategories_user(int(catid), call.from_user.id))


@dp.callback_query_handler(text_contains='usersubcat_')
async def usersubcatcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        subcatid = call.data.split('_')[1]
        if len(db.check_goods(int(subcatid))) == 0:
            await call.answer(translater(call.from_user.id, 'К сожалению тут пусто'), show_alert=True)
        else:
            await call.message.delete()
            await send_good(0, int(subcatid), call.from_user.id)

@dp.callback_query_handler(text_contains='catback_')
async def catbackcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        subcatid = call.data.split('_')[1]
        step = call.data.split('_')[2]
        await send_good(int(step), int(subcatid), call.from_user.id)

@dp.callback_query_handler(text_contains='catnext_')
async def catnextcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        subcatid = call.data.split('_')[1]
        step = call.data.split('_')[2]
        await send_good(int(step), int(subcatid), call.from_user.id)


@dp.callback_query_handler(text_contains='tobox_')
async def toboxcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        mkpa = int(call.message.reply_markup.inline_keyboard[1][1].text.split()[0])
        goodid = call.data.split('_')[1]
        for i in range(mkpa):
            db.add_box(call.from_user.id, int(goodid))
        await call.answer(translater(call.from_user.id, 'Товар добавлен в корзину'), show_alert=True)
        a = call.message.reply_markup
        if a.inline_keyboard[-1][0].callback_data != 'korzina':
            a.add(types.InlineKeyboardButton(translater(call.from_user.id,'Корзина'), callback_data='korzina'))
            await call.message.edit_reply_markup(a)

@dp.callback_query_handler(text_contains='count_')
async def countcall(call: types.CallbackQuery):
    a = call.message.reply_markup
    count = int(a.inline_keyboard[1][1].text.split()[0])
    d = call.data.split('_')[1]
    if d == 'plus':
        a.inline_keyboard[1][1].text = f'{count+1} '+translater(call.from_user.id, 'шт')
    else:
        if count == 1:
            pass
        else:
            a.inline_keyboard[1][1].text = f'{count-1} '+translater(call.from_user.id, 'шт')
    await call.message.edit_reply_markup(a)
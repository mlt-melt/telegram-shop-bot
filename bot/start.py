from config import dp, db
from aiogram import types
from captcha import Captcha
from markups import rules_mkp, menu_mkp
from aiogram.dispatcher import FSMContext
from functions import translater
from states import NewUsername
from functions import anti_flood




@dp.message_handler(commands='start')
@dp.throttled(anti_flood,rate=1)
async def startcmd(message: types.Message):
    
    stat = db.check_userstat(message.from_user.id)
    if len(message.text.split()) == 2:
        db.add_user(message.from_user.id, message.from_user.username, int(message.text.split()[1]))
    else:
        db.add_user(message.from_user.id, message.from_user.username, 0)
    if stat == 'rules':
        await message.answer(db.get_rules(), reply_markup=rules_mkp(message.from_user.id))
    elif stat == 'ban':
        await message.answer(translater(message.from_user.id, 'Вы заблокированы'))
    elif stat == 'ok':
        await message.answer(translater(message.from_user.id, 'Вы в меню'), reply_markup=menu_mkp(message.from_user.id))
    else:
        captcha = Captcha()
        captcha.register_handlers(dp)
        
        await message.answer(
            captcha.get_caption(),
            reply_markup=captcha.get_captcha_keyboard()
        )
        

@dp.message_handler(text='Изменить язык')
@dp.message_handler(text='Change language')
@dp.throttled(anti_flood,rate=1)
async def changelang(message: types.Message):
    db.change_language(message.from_user.id)
    await message.answer(translater(message.from_user.id, 'Вы были возвращены в меню'), reply_markup=menu_mkp(message.from_user.id))
    

@dp.message_handler(commands='id')
@dp.throttled(anti_flood,rate=1)
async def idcmd(message: types.Message):
    await message.answer(f'Ваш ID: <code>{message.from_user.id}</code>')


@dp.callback_query_handler(text='rulesok')
async def rulesokcall(call: types.CallbackQuery):
    await call.message.delete()
    db.change_status(call.from_user.id, 'ok')
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('РУ 🇷🇺', callback_data='language_ru')
    btn2 = types.InlineKeyboardButton('EN 🇺🇸', callback_data='language_en')
    mkp.add(btn1, btn2)
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer('Выберите язык / Choose language', reply_markup=mkp)
    elif check_lan[0] == 1:
        db.update_language(call.from_user.id, 'ru')
        await call.message.answer(translater(call.from_user.id, 'Придумайте и введите свой никнейм:'))
        await NewUsername.Username.set()
    elif check_lan[1] == 1:
        db.update_language(call.from_user.id, 'en')
        await call.message.answer(translater(call.from_user.id, 'Придумайте и введите свой никнейм:'))
        await NewUsername.Username.set()



@dp.callback_query_handler(text_contains='language_')
async def languagecall(call: types.CallbackQuery):
    lan = call.data.split('_')[1]
    db.update_language(call.from_user.id, lan)
    await call.message.answer(translater(call.from_user.id, 'Придумайте и введите свой никнейм:'))
    await NewUsername.Username.set()
    # await call.message.answer(translater(call.from_user.id, 'Вы в меню'), reply_markup=menu_mkp(call.from_user.id))
    


@dp.message_handler(state=NewUsername.Username)
async def newusernameusernamemsg(message: types.Message, state: FSMContext):
    if len(message.text) > 5:
        db.update_usernamerev(message.text, message.from_user.id)
        await state.finish()
        await message.answer(translater(message.from_user.id, 'Вы в меню'), reply_markup=menu_mkp(message.from_user.id))
    else:
        await message.answer(translater(message.from_user.id, 'Минимальная длина ника 6 символов. Попробуйте ещё раз:'))
    

@dp.callback_query_handler(text='rulesno')
async def rulesnocall(call: types.CallbackQuery):
    db.change_status(call.from_user.id, 'ban')
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Вы заблокированы'))
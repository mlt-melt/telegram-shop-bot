from config import dp, db, bot, admins, feedback_channel_id, languageForFeedback
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import ReviewTake
from markups import cancel_mkp, menu_mkp
from functions import translater
import pickle


@dp.callback_query_handler(text_contains='takeotziv_')
async def takeotzivcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Введите оценку от 1 до 5:'), reply_markup=cancel_mkp(call.from_user.id))
    await ReviewTake.OrderId.set()
    async with state.proxy() as data:
        data['OrderId'] = call.data.split('_')[1]
    await ReviewTake.next()

@dp.message_handler(state=ReviewTake.Stars)
async def reviewtakestartmsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) > 0 and int(message.text) < 6:
            async with state.proxy() as data:
                data['Stars'] = message.text
            await message.answer(translater(message.from_user.id, 'Введите ваш отзыв текстом:'), reply_markup=types.InlineKeyboardMarkup(types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')))
            await ReviewTake.next()
        else:
            await message.answer(translater(message.from_user.id, 'Введите оценку от 1 до 5:'), reply_markup=cancel_mkp(message.from_user.id))
    else:
        await message.answer(translater(message.from_user.id, 'Введите оценку числом!'), reply_markup=cancel_mkp(message.from_user.id))

@dp.callback_query_handler(text='cancel', state=ReviewTake.Review)
@dp.callback_query_handler(text='cancel', state=ReviewTake.Stars)
async def reviewtakecancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в меню'), reply_markup=menu_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=ReviewTake.Review)
async def reviewtakereviewmsg(message: types.Message, state: FSMContext):
    try:
        stars_list = ['🌟', '🌟', '🌟🌟', '🌟🌟🌟', '🌟🌟🌟🌟', '🌟🌟🌟🌟🌟']
        async with state.proxy() as data:
            pass
        order_id = data['OrderId']
        stars = data['Stars']
        a = db.get_order_info(int(order_id))[0]
        b = pickle.loads(a)
        text = translater(message.from_user.id, 'Заказ') + f' №{order_id}\n' + translater(message.from_user.id, 'Товар:\n')
        for i in b:
            try:
                a = float(i)
            except:
                text=f'{text} {i}\n'

        res = db.subname_catname(b[0])
        # print(res)
        if db.get_usernamerev(message.from_user.id):
            a = db.get_usernamerev(message.from_user.id)
            b = f'{a[:2]}***{a[-2:]}'
            if languageForFeedback == "en":
                await bot.send_message(feedback_channel_id, f'{text}<b>User</b>: {b}\n<b>Rate</b>: {stars_list[int(stars)]}\n<b>Category</b>: {res[0]}\n<b>Feedback</b>: {message.text}')
            else:
                await bot.send_message(feedback_channel_id, f'{text}<b>Пользователь</b>: {b}\n<b>Оценка</b>: {stars_list[int(stars)]}\n<b>Категория</b>: {res[0]}\n<b>Отзыв</b>: {message.text}')
        else:
            if languageForFeedback == "en":
                await bot.send_message(feedback_channel_id, f'{text}<b>User</b>: {message.from_user.first_name}\n<b>Rate</b>: {stars_list[int(stars)]}\n<b>Category</b>: {res[0]}\n<b>Feedback</b>: {message.text}')
            else:
                await bot.send_message(feedback_channel_id, f'{text}<b>Пользователь</b>: {message.from_user.first_name}\n<b>Оценка</b>: {stars_list[int(stars)]}\n<b>Категория</b>: {res[0]}\n<b>Отзыв</b>: {message.text}')
        reviewpay = db.get_reviewpay()
        if int(reviewpay) == 0:
            pass
        else:
            db.add_balance(message.from_user.id, float(reviewpay))
            await message.answer(translater(message.from_user.id, f'Вам на баланс было начислено') + f' {reviewpay} ' + translater(message.from_user.id, 'руб за отзыв!'))
    except Exception as ex:
        print(ex)
        for admin in admins:
            try:
                await bot.send_message(admin, translater(message.from_user.id, 'Произошла ошибка при отправлении отзыва в канал'))
            except:
                pass
    await message.answer(translater(message.from_user.id, 'Спасибо. Вы были возвращены в меню'), reply_markup=menu_mkp(message.from_user.id))
    await state.finish()

from itertools import count
from config import admins, dp, bot, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import AddSupport, SuppUser, SuppAdmin, QuestAddQuest
from markups import cancel_mkp, menu_mkp, questions_mkp, admin_mkp, menu_mkp_without_sprt_btn, questions_support_mkp
from functions import translater


@dp.message_handler(text='Поддержка ✉️')
@dp.message_handler(text='Support ✉️')
async def suppmsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        check_quest = db.check_questionsusr(message.from_user.id)
        if check_quest == 'ok':
            await message.answer(translater(message.from_user.id, 'Введите свой вопрос и мы ответим в ближайшее время:'), reply_markup=cancel_mkp(message.from_user.id))
            await SuppUser.UserId.set()
        else:
            await message.answer(translater(message.from_user.id, 'Вы можете дополнить свой вопрос. Просто нажмите на кнопку ниже'), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Дополнить вопрос', callback_data=f'addquesttoquest_{check_quest}')))


@dp.callback_query_handler(text='cancel', state=SuppUser.UserId)
async def cancelstatesuppuser(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в меню'), reply_markup=menu_mkp(call.from_user.id))
    await state.finish()


@dp.message_handler(state=SuppUser.UserId)
async def suppuseruseridmsg(message: types.Message, state: FSMContext):
    for admin in admins:
        try:
            await bot.send_message(admin, f'Поступил вопрос от пользователя! Посмотрите его в списках заявок')
        except:
            pass
    
    supports = db.get_supports()
    for support in supports:
        try:
            await bot.send_message(support, f'Поступил вопрос от пользователя! Посмотрите его в списках заявок')
        except:
            pass
    
    await message.answer(translater(message.from_user.id, 'Ваше сообщение отправлено! Ожидайте ответа'))
    question_id = db.add_question(message.from_user.id, message.text)
    await message.answer(translater(message.from_user.id, 'Вы можете дополнить свой вопрос. Просто нажмите на кнопку ниже'), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Дополнить вопрос', callback_data=f'addquesttoquest_{question_id}')))
    await message.answer(translater(message.from_user.id, 'Вы были возвращены в меню'), reply_markup=menu_mkp_without_sprt_btn(message.from_user.id))
    await state.finish()

@dp.callback_query_handler(text_contains='addquesttoquest_')
async def addquesttoquestcall(call: types.CallbackQuery, state: FSMContext):
    questid = call.data.split('_')[1]
    await QuestAddQuest.CountMsg.set()
    await QuestAddQuest.next()
    await call.message.delete()
    async with state.proxy() as data:
        data['CountMsg'] = 0
        data['QuestId'] = questid
    await call.message.answer(translater(call.from_user.id, 'Введите текст и я его отправлю администратору'), reply_markup=cancel_mkp(call.from_user.id))


@dp.message_handler(state=QuestAddQuest.QuestId)
async def questaddquestquestidmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    countmsg = int(data['CountMsg'])
    questid = data['QuestId']
    if countmsg < 3:
        for admin in admins:
            try:
                await bot.send_message(admin, f'Дополнение к вопросу №{questid}\n\n{message.text}')
            except:
                pass

        supports = db.get_supports()
        for support in supports:
            try:
                await bot.send_message(support, f'Дополнение к вопросу №{questid}\n\n{message.text}')
            except:
                pass
        await message.answer(translater(message.from_user.id, 'Введите ещё дополнение к вопросу или нажмите "Отменить"'), reply_markup=cancel_mkp(message.from_user.id))
        countmsg = countmsg+1
        async with state.proxy() as data:
            data['CountMsg'] = countmsg
        db.add_toquest(int(questid), message.text)
        
    elif countmsg == 3:
        for admin in admins:
            try:
                await bot.send_message(admin, f'Дополнение к вопросу №{questid}\n\n{message.text}')
            except:
                pass
        
        for support in supports:
            try:
                await bot.send_message(support, f'Дополнение к вопросу №{questid}\n\n{message.text}')
            except:
                pass
        db.add_toquest(int(questid), message.text)
        await message.answer(translater(message.from_user.id, 'Достигнуто максимальное количество сообщений! Подождите ответа от администратора'), reply_markup=menu_mkp_without_sprt_btn(message.from_user.id))
        await state.finish()
    
@dp.callback_query_handler(text='cancel', state=QuestAddQuest.QuestId)
async def cancelquestaddquest(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Спасибо. Мы скоро вам ответим'), reply_markup=menu_mkp_without_sprt_btn(call.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='answer_')
async def answercall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    
    await call.message.answer('Введите ответ пользователю:')
    await SuppAdmin.UserId.set()
    user_id = call.data.split('_')[1]
    quest_id = call.data.split('_')[2]
    async with state.proxy() as data:
        data['UserId'] = user_id
    await SuppAdmin.next()
    async with state.proxy() as data:
        data['QuestId'] = quest_id
    await SuppAdmin.next()

@dp.message_handler(state=SuppAdmin.Text)
async def suppadminuseridmsg(message: types.Message, state: FSMContext):
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Ждать ответ', callback_data='waitan')
    btn2 = types.InlineKeyboardButton('Завершить', callback_data='endan')
    mkp.add(btn1).add(btn2)
    await message.answer('Сообщение отправлено! Отпрaвьте ещё или нажмите "Завершить" или "Ждать ответ"', reply_markup=mkp)
    async with state.proxy() as data:
        pass
    user_id = data['UserId']
    quest_id = data['QuestId']
    await bot.send_message(int(user_id), translater(int(user_id), 'Ответ от администратора')+f': \n{message.text}')

@dp.callback_query_handler(text='waitan', state=SuppAdmin.Text)
async def waitancall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    user_id = data['UserId']
    quest_id = data['QuestId']
    await call.message.delete()
    await call.message.answer('Пользователь получил уведомление! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    try:
        await bot.send_message(int(user_id), translater(int(user_id), 'Чтобы ответить администратору, нажмите на кнопку ниже:'), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Ответить', callback_data=f'addquesttoquest_{quest_id}')))
    except:
        pass
    await state.finish()
    
@dp.callback_query_handler(text='endan', state=SuppAdmin.Text)
async def endansuppadmincall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        pass
    user_id = data['UserId']
    quest_id = data['QuestId']
    db.del_quest(int(quest_id))
    await call.message.answer('Вопрос закрыт. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(text='Вопросы в поддержку')
async def questionsadmmsg(message: types.Message):
    supports = db.get_supports()
    if message.from_user.id in admins or message.from_user.id in supports:
        await message.answer('Вопросы от пользователей:', reply_markup=questions_mkp())

@dp.message_handler(text='Поддержка')
async def supportFromAdmin(message: types.Message):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Вопросы в поддержку')
    btn2 = types.KeyboardButton('Управлять агентами поддержки')
    btn3 = types.KeyboardButton('Вернуться в админ панель')
    mkp.add(btn1).add(btn2).add(btn3)
    supports = db.get_supports()
    if message.from_user.id in admins or message.from_user.id in supports:
        await message.answer('Вы хотите управлять агентами поддержки или посмотреть новые вопросы пользователей?', reply_markup=mkp)


@dp.message_handler(text='Управлять агентами поддержки')
async def supportFromAdmin(message: types.Message):
    mkp = types.InlineKeyboardMarkup()
    mkp.add(types.InlineKeyboardButton('Добавить агента поддержки', callback_data='add_support'))
    mkp.add(types.InlineKeyboardButton('Удалить агента поддержки', callback_data='del_support'))
    mkp.add(types.InlineKeyboardButton('Вернуться в админ панель', callback_data='admin'))
    supports = db.get_supports()
    supprtsList = ''
    for i in supports:
        supprtsList += f"<code>{i}</code>\n"
    if message.from_user.id in admins or message.from_user.id in supports:
        await message.answer(f'Список агентов:\n{supprtsList}\nВы хотите добавить агента поддержки или удалить одного из них?', reply_markup=mkp)

@dp.callback_query_handler(text='add_support')
async def add_support(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    mkp.add(types.InlineKeyboardButton('Вернуться в админ панель', callback_data='admin'))
    await call.message.answer('Напишите id юзера, которого хотите добавить в агентов поддержки', reply_markup=mkp)
    await AddSupport.UserId.set()

@dp.message_handler(state=AddSupport.UserId)
async def add_support_go(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
        db.update_supports("add", int(user_id))
        await message.answer(f'Юзер {user_id} был добавлен в агенты поддержки')
        await message.answer('Вы были возвращены в админ-панель', reply_markup=admin_mkp())
        await state.finish()
    except:
        await message.answer('Ошибка! Вероятно вы неправильно ввели id. Попробуйте еще раз', reply_markup=cancel_mkp(message.from_user.id))

@dp.callback_query_handler(text='del_support')
async def add_support(call: types.CallbackQuery):
    await call.message.delete()
    supports = db.get_supports()
    mkp = types.InlineKeyboardMarkup()
    for i in supports:
        mkp.add(types.InlineKeyboardButton(i, callback_data=f'del_support_{i}'))
    mkp.add(types.InlineKeyboardButton('Вернуться в админ панель', callback_data='admin'))
    await call.message.answer('Какого агента поддержки вы хотите удалить', reply_markup=mkp)

@dp.callback_query_handler(text_contains='del_support_')
async def del_support_go(call: types.CallbackQuery):
    await call.message.delete()
    user_id = int(call.data.split('_')[2])
    db.update_supports("delete", int(user_id))
    await call.message.answer(f'Юзер {user_id} был удален из агентов поддержки')
    await call.message.answer('Вы были возвращены в админ-панель', reply_markup=admin_mkp())

@dp.message_handler(commands=['support'])
async def questionsadmmsg2(message: types.Message):
    supports = db.get_supports()
    if message.from_user.id in admins or message.from_user.id in supports:
        await message.answer('Вопросы от пользователей:', reply_markup=questions_support_mkp())

@dp.callback_query_handler(text='questions')
async def questionsacall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Вопросы от пользователей:', reply_markup=questions_mkp())

@dp.callback_query_handler(text_contains='question_')
async def questioncall(call: types.CallbackQuery, state: FSMContext):
    questid = call.data.split('_')[1]
    await call.message.delete()
    quest_info = db.get_quest(int(questid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Ответить', callback_data=f'answer_{quest_info[0]}_{questid}')
    btn2 = types.InlineKeyboardButton('Вернуться', callback_data='questions')
    mkp.add(btn1).add(btn2)
    await call.message.answer(f'Вопрос от пользователя с ID: <code>{quest_info[0]}</code> | {db.get_username(int(quest_info[0]))}\n\n{quest_info[1]}', reply_markup=mkp)
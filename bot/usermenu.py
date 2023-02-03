from config import dp, bot, db, bot_url, admins
from aiogram import types
from aiogram.dispatcher import FSMContext
from markups import cancel_mkp, menu_mkp, usermenu_mkp
from states import Withdraw, Deposit
from payments import get_payment, getCoins, createPayment, create_pay
from captcha import Captcha
from functions import translater, anti_flood, torub, rubto
import requests

def get_courses():
    a = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = a.json()['Valute']['USD']['Value']
    eur = a.json()['Valute']['EUR']['Value']
    returns = [usd, eur]
    return returns

@dp.message_handler(text='Меню пользователя 👤')
@dp.message_handler(text='User menu 👤')
@dp.throttled(anti_flood,rate=1)
async def usermenumsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        if db.check_userstat(message.from_user.id) != 'reg':
            curr = db.get_currencysetadm()[0]
            user_id = message.from_user.id
            user_info = db.get_user_info(int(user_id))
            username = user_info[0]
            if username == '' or username == 'None' or username == None:
                username = ''
            else:
                username = translater(message.from_user.id, 'Логин: ') + f'@{username}\n'
            balance = round(rubto(curr, user_info[1]), 2)
            nickname = db.get_usernamerev(message.from_user.id)
            pay_count = user_info[2]
            if pay_count == None:
                pay_count = 0
            userstatus = db.get_userstatus_new(int(user_id))
            db.remove_old_orders()
            await message.answer(translater(message.from_user.id, 'Статус пользователя')+': '+translater(message.from_user.id, userstatus)+'\n-------------------\n'+translater(message.from_user.id ,'Ник: ')+nickname+'\n'+username+translater(message.from_user.id, 'Баланс: ')+str(balance)+' '+str(curr)+'\n'+translater(message.from_user.id, 'Персональная скидка: ')+str(db.get_procent(int(user_id)))+'%\n'+translater(message.from_user.id, f'Купон на скидку: ') + (db.get_promoadm(int(user_id))) +'\n-------------------\n'+translater(message.from_user.id, 'Личная статистика:')+'\n'+translater(message.from_user.id, 'Покупок: ')+str(pay_count)+'\n'+translater(message.from_user.id, 'На сумму: ')+str(round(rubto(curr, db.get_count_buyspr(int(user_id))), 2))+' '+str(curr)+'\n-------------------\n'+translater(message.from_user.id, 'Статистика реф.системы:')+'\n'+translater(message.from_user.id, 'Реф. приглашено: ')+str(db.get_count_refs(int(user_id)))+'\n'+translater(message.from_user.id, 'Реф. заработано: ')+str(round(db.get_refbalance(int(user_id)), 2)))
            await message.answer(translater(message.from_user.id, 'Вы вошли в меню пользователя'), reply_markup=usermenu_mkp(message.from_user.id))
        else:
            captcha = Captcha()
            captcha.register_handlers(dp)
            
            await message.answer(
                captcha.get_caption(),
                reply_markup=captcha.get_captcha_keyboard()
            )



@dp.message_handler(text='Баланс 💰')
@dp.message_handler(text='Balance 💰')
@dp.throttled(anti_flood,rate=1)
async def balancemsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        if db.check_userstat(message.from_user.id) != 'reg':
            curr = db.get_currencysetadm()[0]
            balance = rubto(curr, db.get_balance(message.from_user.id))
            ref_balance = rubto(curr, db.get_refbalance(message.from_user.id))
            mkp = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Пополнить'), callback_data='deposit')
            btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Вывести'), callback_data='withdraw')
            mkp.add(btn1, btn2)
            await message.answer('<b>'+translater(message.from_user.id, 'Ваш баланс')+f'</b>: <code>{float(balance)}</code> {curr}\n<b>'+translater(message.from_user.id, 'Заработано с рефералов')+f'</b>: <code>{float(ref_balance)}</code> {curr}', reply_markup=mkp)
        else:
            captcha = Captcha()
            captcha.register_handlers(dp)
            
            await message.answer(
                captcha.get_caption(),
                reply_markup=captcha.get_captcha_keyboard()
            )

@dp.callback_query_handler(text='deposit')
async def depositcall(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    await call.message.answer(translater(call.from_user.id, 'Введите суму депозита:'), reply_markup=cancel_mkp(call.from_user.id))
    await Deposit.Amount.set()



@dp.message_handler(state=Deposit.Amount)
@dp.throttled(anti_flood,rate=1)
async def depositamountmsg(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        curr = db.get_currencysetadm()[0]
        if curr == 'rub':
            if amount > 499:
                async with state.proxy() as data:
                    data['Amount'] = amount
                qiwistat = db.get_qiwi_stat()
                cryptostat = db.get_crypto_stat()
                yoomoney = db.get_yoomoney_stat()
                print(yoomoney)
                print(cryptostat)
                mkp = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Qiwi', callback_data='depqiwi')
                btn2 = types.InlineKeyboardButton('Yoomoney', callback_data='depyoomoney')
                btn3 = types.InlineKeyboardButton('Crypto', callback_data='depcrypto')
                btn4 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')

                if qiwistat == 'on':
                    mkp.insert(btn1)
                if cryptostat == 'on':
                    mkp.insert(btn3)
                if yoomoney == 'on':
                    mkp.insert(btn2)
                mkp.add(btn4)
                await message.answer(translater(message.from_user.id, 'Выберите способ оплаты:'), reply_markup=mkp)
            else:
                await message.answer(translater(message.from_user.id, 'Минимальная сумма депозита 500 руб. Попробуйте ещё раз'))
        else:
            if amount > 4:
                async with state.proxy() as data:
                    data['Amount'] = amount
                qiwistat = db.get_qiwi_stat()
                cryptostat = db.get_crypto_stat()
                yoomoney = db.get_yoomoney_stat()
                mkp = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Qiwi', callback_data='depqiwi')
                btn2 = types.InlineKeyboardButton('Yoomoney', callback_data='depyoomoney')
                btn3 = types.InlineKeyboardButton('Crypto', callback_data='depcrypto')
                btn4 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')

                if qiwistat == 'on':
                    mkp.insert(btn1)
                if cryptostat == 'on':
                    mkp.insert(btn3)
                if yoomoney == 'on':
                    mkp.insert(btn2)
                mkp.add(btn4)
                await message.answer(translater(message.from_user.id, 'Выберите способ оплаты:'), reply_markup=mkp)
            else:
                await message.answer(translater(message.from_user.id, 'Минимальная сумма депозита 4 usd/eur. Попробуйте ещё раз'))
    except:
        await message.answer(translater(message.from_user.id, 'Вы ввели не число! Введите целое число или число с точкой, например:')+'<code>134.50</code>', reply_markup=cancel_mkp(message.from_user.id))


@dp.callback_query_handler(text='depcrypto', state=Deposit.Amount)
async def depcryptodepamountcall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    amount = data['Amount']
    await call.message.delete_reply_markup()
    await call.answer(translater(call.from_user.id, 'Загружаю список криптовалют'))
    coins = await getCoins()
    mkp = types.InlineKeyboardMarkup(row_width=4)
    for coin in coins:
        mkp.insert(types.InlineKeyboardButton(coin, callback_data=f'cryptodep_{coin}_n_{amount}'))
    await call.message.answer(translater(call.from_user.id, 'Выберите криптовалюту для оплаты'), reply_markup=mkp)
    await state.finish()

@dp.callback_query_handler(text_contains='cryptodep_')
async def cryptodepcall(call: types.CallbackQuery):
    crypto = call.data.split('_')[1]
    amount = call.data.split('_')[3]
    currency = db.get_currencysetadm()[0]
    try:
        paym = await createPayment(amount, crypto, currency)
        pay_amount = paym['pay_amount']
        pay_adress = paym['pay_address']
        pay_currency = paym['pay_currency']
        pay_id = paym['payment_id']
        mkp = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(translater(call.from_user.id, 'Проверить оплату'), callback_data=f'cryptocheck_{pay_id}_n_{amount}')
        mkp.add(btn)
        await call.message.answer(translater(call.from_user.id, 'Переведите')+f': <code>{pay_amount}</code> {pay_currency}\n'+translater(call.from_user.id, 'На кошелек')+f': <code>{pay_adress}</code>\n\n'+translater(call.from_user.id, 'После оплаты не забудьте нажать на "Проверить оплату". Транзакция может проходить до 2-х часов'), reply_markup=mkp)
    except:
        await call.message.answer(translater(call.from_user.id, 'Сумма оплаты ниже минимальной. Попробуйте выполнить депозит на большую сумму'), reply_markup=menu_mkp(call.from_user.id))

@dp.callback_query_handler(text='depyoomoney', state=Deposit.Amount)
async def depyoomoneycall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    amount = data['Amount']
    curr = db.get_currencysetadm()[0]
    amount = torub(curr, amount)
    await call.message.delete_reply_markup()
    payments = create_pay(float(amount), call.from_user.id, 'n')
    paylink = payments[0]
    billid = payments[1]
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Оплатить'), url=paylink)
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Проверить оплату'), callback_data=f'checkpayyoom_n_{amount}_{billid}')
    mkp.add(btn1).add(btn2)
    await call.message.answer(translater(call.from_user.id, 'Оплата создана. Оплатите по кнопке ниже. После оплаты не забудьте нажать на "Проверить оплату"'), reply_markup=mkp)
    await state.finish()


@dp.callback_query_handler(text='depqiwi', state=Deposit.Amount)
async def depqiwicall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    curr = db.get_currencysetadm()[0]
    amount = data['Amount']
    amount = torub(curr, amount)
    await call.message.delete_reply_markup()
    paylink = get_payment(call.from_user.id, 'n', float(amount))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Оплатить'), url=paylink.pay_url)
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Проверить оплату'), callback_data=f'checkpayqiwi_n_{amount}_{paylink.bill_id}')
    mkp.add(btn1).add(btn2)
    await call.message.answer(translater(call.from_user.id, 'Оплата создана. Оплатите по кнопке ниже. После оплаты не забудьте нажать на "Проверить оплату"'), reply_markup=mkp)
    await state.finish()

@dp.callback_query_handler(state=Deposit.Amount, text='cancel')
async def canceldepositamountcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в меню'), reply_markup=menu_mkp(call.from_user.id))
    await state.finish()



@dp.callback_query_handler(text='withdraw')
async def withdrawcall(call: types.CallbackQuery):
    balance = db.get_balance(call.from_user.id)
    if float(balance) > 0:
        await call.message.delete_reply_markup()
        await call.message.answer(translater(call.from_user.id, 'Введите сумму для вывода:'), reply_markup=cancel_mkp(call.from_user.id))
        await Withdraw.Amount.set()
    else:
        await call.answer(translater(call.from_user.id, 'На вашем балансе 0 RUB'), show_alert=True)

@dp.message_handler(state=Withdraw.Amount)
async def withdrawamountmsg(message: types.Message, state: FSMContext):
    try:
        msg = float(message.text)
        bal = float(db.get_balance(message.from_user.id))
        if msg <= bal:
            async with state.proxy() as data:
                data['Amount'] = msg
            await message.answer(translater(message.from_user.id, 'Введите реквизиты, например:')+' <code>Qiwi +7123456789</code>', reply_markup=cancel_mkp(message.from_user.id))
            await Withdraw.next()
        else:
            await message.answer(translater(message.from_user.id, 'Вы ввели большее число, чем у вас имеется! Попробуйте ещё раз'), reply_markup=cancel_mkp(message.from_user.id))
    except:
        await message.answer(translater(message.from_user.id, 'Введите сумму для вывода целым числом или через точку, например:')+' <code>151.21</code>', reply_markup=cancel_mkp(message.from_user.id))

@dp.message_handler(state=Withdraw.Req)
async def withdrawreqmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Req'] = message.text
    amount = data['Amount']
    req = data['Req']
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data='go')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    mkp.add(btn1).add(btn2)
    currency = db.get_currencysetadm()[0]
    await message.answer(translater(message.from_user.id, 'Вы точно хотите подать заявку на вывод')+f' <code>{amount}</code> {currency.upper()}\n'+translater(message.from_user.id, 'На реквизиты')+f': {req}', reply_markup=mkp)

@dp.callback_query_handler(text='go', state=Withdraw.Req)
async def gowithdrawreqcall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    amount = data['Amount']
    currency = db.get_currencysetadm()[0]
    courses = get_courses()
    if currency == "usd":
        amount = float(amount)*float(courses[0])
    elif currency == "eur":
        amount = float(amount)*float(courses[1])
    req = data['Req']
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Заявка на вывод успешно подана. Вы были возвращены в меню'), reply_markup=menu_mkp(call.from_user.id))
    db.pay_balance(call.from_user.id, float(amount))
    db.add_withdraw(call.from_user.id, amount, req)
    await state.finish()
    for admin in admins:
        try:
            await bot.send_message(admin, f'Поступила заявка на вывод. Посмотрите её в админке')
        except:
            pass

@dp.callback_query_handler(text='cancel', state=Withdraw.Req)
@dp.callback_query_handler(text='cancel', state=Withdraw.Amount)
async def cancelwithdraw(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в меню'), reply_markup=menu_mkp(call.from_user.id))
    await state.finish()


@dp.message_handler(text='Реферальная система 👥')
@dp.message_handler(text='Refferal system 👥')
@dp.throttled(anti_flood,rate=1)
async def refsystemmsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        if db.check_userstat(message.from_user.id) != 'reg':
            ref = db.get_refproc_for_user(message.from_user.id)
            count_ref = db.get_all_refs(message.from_user.id)
            await message.answer(translater(message.from_user.id, 'Ваша реф ссылка')+f': <code>{bot_url}?start={message.from_user.id}</code>\n\n'+translater(message.from_user.id, 'Вы получите')+f' {ref}% '+translater(message.from_user.id, 'с покупок реферала\n\nВсего приглашено')+f': {len(count_ref)}')
        else:
            captcha = Captcha()
            captcha.register_handlers(dp)
            
            await message.answer(
                captcha.get_caption(),
                reply_markup=captcha.get_captcha_keyboard()
            )

@dp.message_handler(text='Мои покупки 📦')
@dp.message_handler(text='My purchases 📦')
@dp.throttled(anti_flood,rate=1)
async def myordersmsg(message: types.Message):
    if db.check_ban(message.from_user.id):
        if db.check_userstat(message.from_user.id) != 'reg':
            active_order = db.get_actorders(message.from_user.id)
            end_orders = db.get_endorders(message.from_user.id)
            wait_orders = db.get_waitorders(message.from_user.id)
            db.remove_old_orders()
            if len(active_order) == 0:
                await message.answer(translater(message.from_user.id, 'Активных заказов не обнаружено'))
            else:
                text = ''
                for i in active_order:
                    text=f'{text}---------------------\n'
                    step = 1
                    for a in i:
                        try:
                            curr = db.get_currencysetadm()[0]
                            if curr == 'rub':
                                price = float(a)
                            else:
                                price = rubto(curr, float(a))
                                price = float(price)
                                price = f'{price:.2f}'
                            text=f'{text}'+translater(message.from_user.id, 'Сумма')+f': {float(price)}\n'
                        except:
                            text=f'{text}{step}.{i[0]}\n'
                        step=step+1
                await message.answer(translater(message.from_user.id, 'Активные заказы')+f':\n{text}')
        
            if len(end_orders) == 0:
                await message.answer(translater(message.from_user.id, 'Завершенных заказов не обнаружено'))
            else:
                text = ''
                for i in end_orders:
                    text=f'{text}---------------------\n'
                    step = 1
                    for a in i:
                        try:
                            curr = db.get_currencysetadm()[0]
                            if curr == 'rub':
                                price = float(a)
                            else:
                                price = rubto(curr, float(a))
                                price = float(price)
                                price = f'{price:.2f}'
                            text=f'{text}'+translater(message.from_user.id, 'Сумма')+f': {float(price)}\n'
                        except:
                            text=f'{text}{step}. {i[0]}\n'
                        step=step+1
                await message.answer(translater(message.from_user.id, 'Последние 2 завершенных заказа')+f':\n{text}')
            try:
                if len(wait_orders[0]) > 0:
                    text=''
                    text=f'{text}---------------------\n'
                    step = 1
                    for a in wait_orders[0][0]:
                        try:
                            curr = db.get_currencysetadm()[0]
                            if curr == 'rub':
                                price = float(a)
                            else:
                                price = rubto(curr, float(a))
                                price = float(price)
                                price = f'{price:.2f}'
                            text=f'{text}\n'+translater(message.from_user.id, 'Итоговая сумма')+f': {float(price)}\n'
                        except:
                            text=f'{text}{step}. {a}\n'
                        step+=1
                    
                    replyMkp = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Проверить оплату'), callback_data=wait_orders[1])
                    replyMkp.add(btn1)

                    await message.answer(translater(message.from_user.id, 'Заказ, ожидающий оплаты:')+f'\n{text}---------------------\nРевизиты для оплаты ниже')
                    await bot.copy_message(message.from_user.id, message.from_user.id, int(db.get_reply_id(wait_orders[1])), reply_markup=replyMkp)

            except:
                pass
        else:
            captcha = Captcha()
            captcha.register_handlers(dp)
            
            await message.answer(
                captcha.get_caption(),
                reply_markup=captcha.get_captcha_keyboard()
            )
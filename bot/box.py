from config import dp, bot, db, admins
from aiogram import types
from aiogram.dispatcher import FSMContext
from markups import cancel_mkp, menu_mkp, deliveryuser_mkp
from states import NewOrder
from captcha import Captcha
from payments import get_payment, check_payment, getCoins, createPayment, check_pay, create_pay, check_pay_yoo
from functions import translater, anti_flood, torub
import asyncio

discountList = [95, 90, 85]

@dp.message_handler(text='Корзина 🛒')
@dp.message_handler(text='Box 🛒')
@dp.throttled(anti_flood,rate=1)
async def boxmsg(message: types.Message):
    if db.check_userstat(message.from_user.id) != 'reg':
        box = db.get_box(message.from_user.id)
        if len(box) == 0:
            await message.answer(translater(message.from_user.id,'Корзина пуста. Перейдите в магазин для совершения покупок'))
        else:
            step = 1
            price = 0
            text = ''
            for i in box:
                try:
                    good_info = db.get_good_info(i[0], message.from_user.id)
                    text = f'{text}{step}. <b>'+translater(message.from_user.id,'Товар')+f'</b>: <code>{good_info[0]}</code> | <b>'+translater(message.from_user.id,'Цена')+f'</b>: {round(float(good_info[1]), 2)}\n'
                    price = price+float(good_info[1])
                    step=step+1
                except:
                    db.del_box_good(int(i[0]))
            price = f'{price:.2f}'
            curr = db.get_currencysetadm()[0]
            text=translater(message.from_user.id, 'Ваша корзина')+f':\n{text}\n\n<b>'+translater(message.from_user.id, 'Итого')+f'</b>: <code>{price}</code> <b>{curr.upper()}</b>'
            mkp = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Оформить заказ'), callback_data='goorder')
            btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Очистить корзину'), callback_data='boxclear')
            mkp.add(btn1).add(btn2)
            await message.answer(text, reply_markup=mkp)
    else:
        captcha = Captcha()
        captcha.register_handlers(dp)
        
        await message.answer(
            captcha.get_caption(),
            reply_markup=captcha.get_captcha_keyboard()
        )


@dp.callback_query_handler(text='korzina')
async def korzinacall(call: types.CallbackQuery):
    await call.message.delete()
    box = db.get_box(call.from_user.id)
    if len(box) == 0:
        await call.message.answer(translater(call.from_user.id, 'Корзина пуста. Перейдите в магазин для совершения покупок'))
    else:
        step = 1
        price = 0
        text = ''
        for i in box:
            try:
                good_info = db.get_good_info(i[0], call.from_user.id)
                text = f'{text}{step}. <b>'+translater(call.from_user.id,'Товар')+f'</b>: <code>{good_info[0]}</code> | <b>'+translater(call.from_user.id, 'Цена')+f'</b>: {round(float(good_info[1]), 2)}\n'
                price = price+float(good_info[1])
                step=step+1
            except:
                await call.message.answer(Exception)
                db.del_box_good(int(i[0]))
        curr = db.get_currencysetadm()[0]
        text=translater(call.from_user.id, 'Ваша корзина')+f':\n{text}\n\n<b>'+translater(call.from_user.id, 'Итого')+f'</b>: <code>{price:.2f}</code> <b>{curr.upper()}</b>'
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Оформить заказ'), callback_data='goorder')
        btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Очистить корзину'), callback_data='boxclear')
        mkp.add(btn1).add(btn2)
        await call.message.answer(text, reply_markup=mkp)


@dp.callback_query_handler(text='boxclear')
async def boxclearcall(call: types.CallbackQuery):
    await call.message.delete()
    db.boxlclear(call.from_user.id)
    await call.message.answer(translater(call.from_user.id, 'Корзина успешно очищена!'), reply_markup=menu_mkp(call.from_user.id))




@dp.callback_query_handler(text='goorder')
async def goordercall(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    await NewOrder.Delivery.set()
    await call.message.answer(translater(call.from_user.id, 'Выберите способ доставки:'), reply_markup=deliveryuser_mkp(call.from_user.id))

@dp.callback_query_handler(text_contains='delivery_', state=NewOrder.Delivery)
async def goordercall(call: types.CallbackQuery, state: FSMContext):
    delivery_id = call.data.split('_')[1]
    async with state.proxy() as data:
        data['Delivery'] = delivery_id
    await call.message.delete()
    await NewOrder.next()
    await call.message.answer(translater(call.from_user.id, 'Введите адрес доставки:'), reply_markup=cancel_mkp(call.from_user.id))

@dp.callback_query_handler(text='cancel', state=NewOrder.Delivery)
@dp.callback_query_handler(text='cancel', state=NewOrder.Comment)
@dp.callback_query_handler(text='cancel', state=NewOrder.Adress)
@dp.callback_query_handler(text='cancel', state=NewOrder.Promo)
async def neworderadresscancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в меню'), reply_markup=menu_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=NewOrder.Adress)
async def neworderadressmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Adress'] = message.text
    
    await message.answer(translater(message.from_user.id, 'Введите комментарий к заказу'), reply_markup=cancel_mkp(message.from_user.id))
    await NewOrder.next()



@dp.message_handler(state=NewOrder.Comment)
async def newordercommentmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Comment'] = message.text
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Пропустить'), callback_data='skip')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer(translater(message.from_user.id, 'Хорошо, введите промокод или нажмите "Пропустить"'), reply_markup=mkp)
    await NewOrder.next()

@dp.message_handler(state=NewOrder.Promo)
async def neworderpromomsg(message: types.Message, state: FSMContext):
    check_promo = db.check_promo(message.text, message.from_user.id)
    if check_promo == None:
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Пропустить'), callback_data='skip')
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
        mkp.add(btn1).add(btn2)
        await message.answer(translater(message.from_user.id, 'Данного промокода не существует или он принадлежит не вам! Введите другой или нажмите "Пропустить"'), reply_markup=mkp)
    else:
        procent = check_promo[0]
        async with state.proxy() as data:
            data['Promo'] = procent
        await message.answer(translater(message.from_user.id, 'Промокод на скидку')+f' {procent}% '+translater(message.from_user.id, 'активирован!'))
        procent = int(data['Promo'])
        procent = 100-procent-db.get_procent(message.from_user.id)
        box = db.get_box(message.from_user.id)
        step = 1
        price = 0
        text = ''
        for i in box:
            try:
                good_info = db.get_good_info(i[0], message.from_user.id)
                text = f'{text}{step}. <b>'+translater(message.from_user.id, 'Товар')+f'</b>: <code>{good_info[0]}</code> | <b>'+translater(message.from_user.id, 'Цена')+f'</b>: {round(float(good_info[1]), 2)}\n'
                price = price+float(good_info[1])
                step=step+1
            except:
                db.del_box_good(int(i[0]))
        delivery = data['Delivery']
        delinfo = db.get_delivery_infouser(int(delivery), int(message.from_user.id))
        price=price+float(delinfo[1])
        price=price/100*procent
        adress = data['Adress']
        comment = data['Comment']
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Qiwi', callback_data='payqiwi')
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Криптовалюта'), callback_data='paycrypto')
        btn3 = types.InlineKeyboardButton('Yoomoney', callback_data='payyoomoney')
        btn4 = types.InlineKeyboardButton(translater(message.from_user.id, 'С баланса'), callback_data='paybalance')
        btn5 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
        qiwistat = db.get_qiwi_stat()
        cryptostat = db.get_crypto_stat()
        yoomoneystat = db.get_yoomoney_stat()
        # mkp.add(btn1, btn2).add(btn3).add(btn4)
        if qiwistat == 'on':
            mkp.insert(btn1)
        if cryptostat == 'on':
            mkp.insert(btn2)
        if yoomoneystat == 'on':
            mkp.insert(btn3)
        mkp.add(btn4).add(btn5)
        await message.answer('<b>'+translater(message.from_user.id, 'Ваш заказ')+f'</b>:\n{text}' + translater(message.from_user.id, 'Доставка: ') + f'{delinfo[0]} ({delinfo[1]})\n\n<b>'+translater(message.from_user.id, 'Итого к оплате')+f'</b>: <code>{float(price)}</code>\n\n<b>'+translater(message.from_user.id, 'Адрес доставки')+f'</b>: <code>{adress}</code>\n<b>'+translater(message.from_user.id, 'Способ доствки')+f'</b>: {delinfo[0]}\n<b>'+translater(message.from_user.id, 'Комментарий')+f'</b>: <code>{comment}</code>')
        await message.answer(translater(message.from_user.id, 'Выберите способ оплаты:'), reply_markup=mkp)

@dp.callback_query_handler(text='skip', state=NewOrder.Promo)
async def neworderpromoskipcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        data['Promo'] = 0
    procent = int(data['Promo'])
    procent = 100-procent-db.get_procent(call.from_user.id)
    box = db.get_box(call.from_user.id)
    step = 1
    price = 0
    text = ''
    for i in box:
        try:
            good_info = db.get_good_info(i[0], call.from_user.id)
            text = f'{text}{step}. <b>'+translater(call.from_user.id, 'Товар')+f'</b>: <code>{good_info[0]}</code> | <b>'+translater(call.from_user.id, 'Цена')+f'</b>: {round(float(good_info[1]), 2)}\n'
            price = price+float(good_info[1])
            step=step+1
        except:
            db.del_box_good(int(i[0]))
    delivery = data['Delivery']
    delinfo = db.get_delivery_infouser(int(delivery), call.from_user.id)
    price=price+float(delinfo[1])
    price=price/100*procent
    adress = data['Adress']
    comment = data['Comment']
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Qiwi', callback_data='payqiwi')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Криптовалюта'), callback_data='paycrypto')
    btn3 = types.InlineKeyboardButton('Yoomoney', callback_data='payyoomoney')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'С баланса'), callback_data='paybalance')
    btn5 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='cancel')
    qiwistat = db.get_qiwi_stat()
    cryptostat = db.get_crypto_stat()
    yoomoneystat = db.get_yoomoney_stat()
    # mkp.add(btn1, btn2).add(btn3).add(btn4)
    if qiwistat == 'on':
        mkp.insert(btn1)
    if cryptostat == 'on':
        mkp.insert(btn2)
    if yoomoneystat == 'on':
        mkp.insert(btn3)
    mkp.add(btn4).add(btn5)
    await call.message.answer('<b>'+translater(call.from_user.id, 'Ваш заказ')+f'</b>:\n{text}' + translater(call.from_user.id, 'Доставка: ') + f'{delinfo[0]} ({delinfo[1]})\n\n<b>'+translater(call.from_user.id, 'Итого к оплате')+f'</b>: <code>{float(price)}</code>\n\n<b>'+translater(call.from_user.id, 'Адрес доставки')+f'</b>: <code>{adress}</code>\n<b>'+translater(call.from_user.id, 'Способ доствки')+f'</b>: {delinfo[0]}\n<b>'+translater(call.from_user.id, 'Комментарий')+f'</b>: <code>{comment}</code>')
    await call.message.answer(translater(call.from_user.id, 'Выберите способ оплаты:'), reply_markup=mkp)


@dp.callback_query_handler(text='paycrypto', state=NewOrder.Promo)
async def paycryptocall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.answer(translater(call.from_user.id, 'Загружаю список криптовалют'))
    coins = await getCoins()
    box = db.get_box(call.from_user.id)
    order = []
    price = 0
    for i in box:
        try:
            good_info = db.get_good_info(i[0], call.from_user.id)
            order.append(good_info[0])
            
            price = price+float(good_info[1])
    
        except:
            db.del_box_good(int(i[0]))
    async with state.proxy() as data:
        pass
    procent = int(data['Promo'])
    procent = 100-procent-db.get_procent(call.from_user.id)
    delivery = data['Delivery']
    adress = data['Adress']
    delinfo = db.get_delivery_infouser(int(delivery), call.from_user.id)
    price=price+float(delinfo[1])
    price=price/100*procent
    adress = translater(call.from_user.id, 'Способ доставки')+f': {delinfo[0]}\n'+translater(call.from_user.id, 'Адрес')+f': {adress}'
    comment = data['Comment']
    order.append(price)
    order_id = db.add_order(call.from_user.id, order, adress, comment)
    mkp = types.InlineKeyboardMarkup(row_width=4)
    for coin in coins:
        mkp.insert(types.InlineKeyboardButton(coin, callback_data=f'crypto_{coin}_{order_id}_{price}'))
    db.boxlclear(call.from_user.id)
    await call.message.answer(translater(call.from_user.id, 'Выберите криптовалюту для оплаты'), reply_markup=mkp)
    await state.finish()


@dp.callback_query_handler(text_contains='crypto_')
async def cryptocall(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    crypto = call.data.split('_')[1]
    order_id = call.data.split('_')[2]
    price = call.data.split('_')[3]
    currency = db.get_currencysetadm()[0]
    try:
        paym = await createPayment(price, crypto, currency)
        pay_amount = paym['pay_amount']
        pay_adress = paym['pay_address']
        pay_currency = paym['pay_currency']
        pay_id = paym['payment_id']
        mkp = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(translater(call.from_user.id, 'Проверить оплату'), callback_data=f'cryptocheck_{pay_id}_{order_id}_{price}')
        db.upd_ordertype(int(order_id), f'cryptocheck_{pay_id}_{order_id}_{price}')
        mkp.add(btn)
        msgForId = await call.message.answer(translater(call.from_user.id, 'Переведите')+f': <code>{pay_amount}</code> {pay_currency}\n'+translater(call.from_user.id, 'На кошелек')+f': <code>{pay_adress}</code>\n\n'+translater(call.from_user.id, 'После оплаты не забудьте нажать на "Проверить оплату". Транзакция может проходить до 2-х часов'), reply_markup=mkp)
        msgId = msgForId["message_id"]
        db.upd_msg_id(int(order_id), msgId)
        times = 30
        while times>0:
            status = await check_pay(pay_id)
            if status == 'confirmed' or status == 'sending' or status == 'finished':
                if db.get_order_status(int(order_id)) == 'wait':
                    await call.message.delete()
                    # await bot.unpin_all_chat_messages(chat_id = call.from_user.id)
                    db.pay_order(int(order_id))
                    for admin in admins:
                        try:
                            await bot.send_message(admin, 'Новый заказ. Оплата криптовалютой. Посмотрите через админ-панель')
                        except:
                            pass
                    ref = db.get_referal(call.from_user.id)
                    refp = db.get_refproc_for_user(call.from_user.id)
                    if ref == 0:
                        pass
                    else:
                        refprice = float(price)/100*float(refp)
                        try:
                            await bot.send_message(int(ref), f'Ваш реферал оформил заказ. Вы получили {round(refprice, 2)} RUB на баланс')
                            db.add_balance(int(ref), refprice)
                            db.add_refbalance(int(ref), refprice)
                        except:
                            pass
                times=0
            else:
                times=times-2
                await asyncio.sleep(120)

    except Exception as ex:
        await call.message.answer(translater(call.from_user.id, f'Сумма оплаты ниже минимальной. Попробуйте добавить ещё товар в корзину'), reply_markup=menu_mkp(call.from_user.id))
        await call.message.answer(translater(call.from_user.id, f'Произошла ошибка:\n<b>{ex}</b>\nОбратитесь к администратору'), parse_mode="html")

@dp.callback_query_handler(text_contains='cryptocheck_')
async def cryptocheckcall(call: types.CallbackQuery):
    a = call.message.reply_markup
    await call.message.delete_reply_markup()
    pay_id = call.data.split('_')[1]
    order_id = call.data.split('_')[2]
    price = call.data.split('_')[3]
    status = await check_pay(pay_id)
    if order_id != 'n':
        if status == 'confirmed' or status == 'sending' or status == 'finished':
            await call.message.answer(translater(call.from_user.id, 'Оплата найдена, менеджер был уведомлен'), reply_markup=menu_mkp(call.from_user.id))
            # await bot.unpin_all_chat_messages(chat_id = call.from_user.id)
            db.pay_order(int(order_id))
            for admin in admins:
                try:
                    await bot.send_message(admin, 'Новый заказ. Оплата криптовалютой. Посмотрите через админ-панель')
                except:
                    pass
            ref = db.get_referal(call.from_user.id)
            refp = db.get_refproc_for_user(call.from_user.id)
            if ref == 0:
                pass
            else:
                refprice = float(price)/100*float(refp)
                try:

                    await bot.send_message(int(ref), f'Ваш реферал оформил заказ. Вы получили {round(refprice, 2)} RUB на баланс')
                    db.add_balance(int(ref), refprice)
                    db.add_refbalance(int(ref), refprice)
                except:
                    pass
        else:
            await call.answer(translater(call.from_user.id, 'Оплата не найдена, попробуйте через 5 минут'), show_alert=True)
            await call.message.edit_reply_markup(a)
    else:
        if status == 'confirmed' or status == 'sending' or status == 'finished':
            await call.message.answer(f'Оплата найдена, ваш баланс был пополнен на {price} RUB', reply_markup=menu_mkp(call.from_user.id))
            db.add_balance(call.from_user.id, float(price))
        else:
            await call.answer(translater(call.from_user.id, 'Оплата не найдена, попробуйте через 5 минут'), show_alert=True)
            await call.message.edit_reply_markup(a)



@dp.callback_query_handler(text='paybalance', state=NewOrder.Promo)
async def paybalancecall(call: types.CallbackQuery, state: FSMContext):
    userbal = db.get_balance(call.from_user.id)
    box = db.get_box(call.from_user.id)
    order = []
    price = 0
    curr = db.get_currencysetadm()[0]
    for i in box:
        try:
            good_info = db.get_good_info(i[0], call.from_user.id)
            order.append(good_info[0])
            price = price+float(good_info[1])
        except:
            db.del_box_good(int(i[0]))
    async with state.proxy() as data:
        pass
    delivery = data['Delivery']
    adress = data['Adress']
    procent = int(data['Promo'])
    procent = 100-procent-db.get_procent(call.from_user.id)
    delinfo = db.get_delivery_infouser(int(delivery), call.from_user.id)
    price=price+float(delinfo[1])
    price=price/100*procent
    price = torub(curr, price)
    adress = translater(call.from_user.id, 'Способ доставки')+f': {delinfo[0]}\n'+translater(call.from_user.id, 'Адрес')+f': {adress}'
    comment = data['Comment']
    order.append(price)
    if float(userbal) < price:
        await call.answer(translater(call.from_user.id, 'На вашем балансе недостаточно средств! Баланс')+f': {float(userbal)} RUB', show_alert=True)
    else:
        await call.message.delete()
        db.pay_balance(call.from_user.id, price)
        await call.message.answer(translater(call.from_user.id, 'Деньги списаны с баланса. Заказ оплачен, менеджер получил уведомление.'), reply_markup=menu_mkp(call.from_user.id))
        order_id = db.add_order(call.from_user.id, order, adress, comment)
        db.boxlclear(call.from_user.id)
        # await bot.unpin_all_chat_messages(chat_id = call.from_user.id)
        db.pay_order(int(order_id))
        for admin in admins:
            try:
                await bot.send_message(admin, 'Новый заказ. Оплата с баланса. Посмотрите через админ-панель')
            except:
                pass
        ref = db.get_referal(call.from_user.id)
        refp = db.get_refproc_for_user(call.from_user.id)
        if ref == 0:
            pass
        else:
            refprice = float(price)/100*float(refp)
            try:

                await bot.send_message(int(ref), f'Ваш реферал оформил заказ. Вы получили {round(refprice, 2)} RUB на баланс')
                db.add_balance(int(ref), refprice)
                db.add_refbalance(int(ref), refprice)
            except:
                pass
        await state.finish()
    

@dp.callback_query_handler(text='payyoomoney', state=NewOrder.Promo)
async def payyoomoneycall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    box = db.get_box(call.from_user.id)
    order = []
    price = 0
    curr = db.get_currencysetadm()[0]
    for i in box:
        try:
            good_info = db.get_good_info(i[0], call.from_user.id)
            order.append(good_info[0])
            price = price+float(good_info[1])
        except:
            db.del_box_good(int(i[0]))
    async with state.proxy() as data:
        pass
    delivery = data['Delivery']
    adress = data['Adress']
    procent = int(data['Promo'])
    procent = 100-procent-db.get_procent(call.from_user.id)
    delinfo = db.get_delivery_infouser(int(delivery), call.from_user.id)
    price=price+float(delinfo[1])
    price=price/100*procent
    price = torub(curr, price)
    adress = translater(call.from_user.id, 'Способ доставки')+f': {delinfo[0]}\n'+translater(call.from_user.id, 'Адрес')+f': {adress}'
    comment = data['Comment']
    order.append(price)
    order_id = db.add_order(call.from_user.id, order, adress, comment)
    paylink = create_pay(price, call.from_user.id, order_id)
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Оплатить'), url=paylink)
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Проверить оплату'), callback_data=f'checkpayqiwi_{order_id}_{price}')
    db.upd_ordertype(int(order_id), f'checkpayyoom_{order_id}_{price}')
    mkp.add(btn1).add(btn2)
    db.boxlclear(call.from_user.id)
    msgForId = await call.message.answer(translater(call.from_user.id, 'Заказ создан. Оплатите через кнопку ниже. После оплаты не забудьте нажать на "Проверить оплату"'), reply_markup=mkp)
    msgId = msgForId["message_id"]
    db.upd_msg_id(int(order_id), msgId)
    await state.finish()

@dp.callback_query_handler(text='payqiwi', state=NewOrder.Promo)
async def payqiwicall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    box = db.get_box(call.from_user.id)
    order = []
    price = 0
    curr = db.get_currencysetadm()[0]
    for i in box:
        try:
            good_info = db.get_good_info(i[0], call.from_user.id)
            order.append(good_info[0])
            price = price+float(good_info[1])
        except:
            db.del_box_good(int(i[0]))
    async with state.proxy() as data:
        pass
    delivery = data['Delivery']
    adress = data['Adress']
    procent = int(data['Promo'])
    procent = 100-procent-db.get_procent(call.from_user.id)
    delinfo = db.get_delivery_infouser(int(delivery), call.from_user.id)
    price=price+float(delinfo[1])
    price=price/100*procent
    price = torub(curr, price)
    adress = translater(call.from_user.id, 'Способ доставки')+f': {delinfo[0]}\n'+translater(call.from_user.id, 'Адрес')+f': {adress}'
    comment = data['Comment']
    order.append(price)
    order_id = db.add_order(call.from_user.id, order, adress, comment)
    paylink = get_payment(call.from_user.id, order_id, price)
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Оплатить'), url=paylink)
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Проверить оплату'), callback_data=f'checkpayqiwi_{order_id}_{price}')
    db.upd_ordertype(int(order_id), f'checkpayqiwi_{order_id}_{price}')
    mkp.add(btn1).add(btn2)
    db.boxlclear(call.from_user.id)
    msgForId = await call.message.answer(translater(call.from_user.id, 'Заказ создан. Оплатите через кнопку ниже. После оплаты не забудьте нажать на "Проверить оплату"'), reply_markup=mkp)
    msgId = msgForId["message_id"]
    db.upd_msg_id(int(order_id), msgId)
    await state.finish()

    times = 30
    while times>0:
        try:
            bill = f'{call.from_user.id}_{order_id}'
            if check_payment(bill) == 'pay':
                if db.get_order_status(int(order_id)) == 'wait':
                    await call.message.delete()
                    await call.message.answer(translater(call.from_user.id, 'Оплата найдена, я передал ваш заказ менеджеру.'), reply_markup=menu_mkp(call.from_user.id))
                    # await bot.unpin_all_chat_messages(chat_id = call.from_user.id)
                    db.pay_order(int(order_id))
                    for admin in admins:
                        try:
                            await bot.send_message(admin, 'Новый заказ. Оплата с киви. Посмотрите через админ-панель')
                        except:
                            pass
                    ref = db.get_referal(call.from_user.id)
                    refp = db.get_refproc_for_user(call.from_user.id)
                    if ref == 0:
                        pass
                    else:
                        refprice = float(price)/100*float(refp)
                        try:

                            await bot.send_message(int(ref), f'Ваш реферал оформил заказ. Вы получили {round(refprice, 2)} RUB на баланс')
                            db.add_balance(int(ref), refprice)
                            db.add_refbalance(int(ref), refprice)
                        except:
                            pass
        except:
            pass

@dp.callback_query_handler(text_contains='checkpayyoom_')
async def checkpayyoomcall(call: types.CallbackQuery):
    order_id = call.data.split('_')[1]
    price = call.data.split('_')[2]
    try:
        if order_id != 'n':
            if check_pay_yoo(call.from_user.id, order_id, '1') == 'pay':
                await call.message.delete()
                await call.message.answer(translater(call.from_user.id, 'Оплата найдена, я передал ваш заказ менеджеру.'), reply_markup=menu_mkp(call.from_user.id))
                # await bot.unpin_all_chat_messages(chat_id = call.from_user.id)
                db.pay_order(int(order_id))
                for admin in admins:
                    try:
                        await bot.send_message(admin, 'Новый заказ. Оплата с юмани. Посмотрите через админ-панель')
                    except:
                        pass
                ref = db.get_referal(call.from_user.id)
                refp = db.get_refproc_for_user(call.from_user.id)
                if ref == 0:
                    pass
                else:
                    refprice = float(price)/100*float(refp)
                    try:

                        await bot.send_message(int(ref), f'Ваш реферал оформил заказ. Вы получили {round(refprice, 2)} RUB на баланс')
                        db.add_balance(int(ref), refprice)
                        db.add_refbalance(int(ref), refprice)
                    except:
                        pass
            else:
                await call.answer(translater(call.from_user.id, 'Оплата не найдена. Проверьте через 5 минут'), show_alert=True)
        else:
            bill = call.data.split('_')[3]+'_'+call.data.split('_')[4]
            if check_pay_yoo('1', '1', bill) == 'pay':
                await call.message.delete()
                await call.message.answer(f'На ваш баланс было зачислено {price} RUB', reply_markup=menu_mkp(call.from_user.id))
                db.add_balance(call.from_user.id, float(price))
            else:
                await call.answer(translater(call.from_user.id, 'Оплата не найдена. Проверьте через 5 минут'), show_alert=True)
    except:
        await call.message.answer('Произошла ошибка, попробуйте позже')

@dp.callback_query_handler(text_contains='checkpayqiwi_')
async def checkpayqiwicall(call: types.CallbackQuery):
    order_id = call.data.split('_')[1]
    price = call.data.split('_')[2]
    bill = f'{call.from_user.id}_{order_id}'
    try:
        if order_id != 'n':
            if check_payment(bill) == 'pay':
                await call.message.delete()
                await call.message.answer(translater(call.from_user.id, 'Оплата найдена, я передал ваш заказ менеджеру.'), reply_markup=menu_mkp(call.from_user.id))
                # await bot.unpin_all_chat_messages(chat_id = call.from_user.id)
                db.pay_order(int(order_id))
                for admin in admins:
                    try:
                        await bot.send_message(admin, 'Новый заказ. Оплата с киви. Посмотрите через админ-панель')
                    except:
                        pass
                ref = db.get_referal(call.from_user.id)
                refp = db.get_refproc_for_user(call.from_user.id)
                if ref == 0:
                    pass
                else:
                    refprice = float(price)/100*float(refp)
                    try:

                        await bot.send_message(int(ref), f'Ваш реферал оформил заказ. Вы получили {round(refprice, 2)} RUB на баланс')
                        db.add_balance(int(ref), refprice)
                        db.add_refbalance(int(ref), refprice)
                    except:
                        pass
            else:
                await call.answer(translater(call.from_user.id, 'Оплата не найдена. Проверьте через 5 минут'), show_alert=True)
        else:
            bill = call.data.split('_')[3]
            if check_payment(bill) == 'pay':
                await call.message.delete()
                await call.message.answer(f'На ваш баланс было зачислено {price} RUB', reply_markup=menu_mkp(call.from_user.id))
                db.add_balance(call.from_user.id, float(price))
            else:
                await call.answer(translater(call.from_user.id, 'Оплата не найдена. Проверьте через 5 минут'), show_alert=True)
    except:
        await call.message.answer('Произошла ошибка, попробуйте позже')
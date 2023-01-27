from config import db, bot
from aiogram import types
import requests
from english import english
from russian import russian


def translater(user_id, text):
    user_id = int(user_id)
    lan = db.get_langugage(user_id)
    try:
        if lan == 'ru':
            if db.check_lan_on(lan) == 'ok':
                return text
            else:
                try:
                    return english[russian.index(text)]
                except:
                    return text
        elif lan == 'en':
            
            if db.check_lan_on(lan) == 'ok' and lan == 'en':
                try:
                    return english[russian.index(text)]
                except:
                    return text
            else:
                return text
    except:
        return text

def get_faq_admin(admin_id):
    faq_list = db.get_all_faq_adm()
    mkp = types.InlineKeyboardMarkup()
    for i in faq_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'changefaq_{i[0]}'))
    mkp.add(types.InlineKeyboardButton(translater(admin_id, 'Новый раздел'), callback_data='newfaq'))
    mkp.add(types.InlineKeyboardButton(translater(admin_id, 'Вернуться в админ-панель'), callback_data='admin'))
    return mkp


def get_faq_user(user_id):
    faq_list = db.get_all_faq(user_id)
    mkp = types.InlineKeyboardMarkup()
    for i in faq_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'getfaq_{i[0]}'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Вернуться в меню'), callback_data='tomenu'))
    return mkp


def get_categories_admin(admin_id):
    cat_list = db.get_all_cat_adm()
    mkp = types.InlineKeyboardMarkup()
    for i in cat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'admincat_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('➕ ' + translater(admin_id, 'Добавить категорию'), callback_data='addcat'))
    mkp.add(types.InlineKeyboardButton('🔙 ' + translater(admin_id, 'Вернуться в админ-панель'), callback_data='admin'))
    return mkp

def get_categories_user(user_id):
    cat_list = db.get_all_cat(user_id)
    mkp = types.InlineKeyboardMarkup()
    for i in cat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'usercat_{i[0]}'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Вернуться в меню'), callback_data='tomenu'))
    return mkp

def get_subcategories_admin(cat_id, admin_id):
    subcat_list = db.get_subcat_adm(cat_id)
    mkp = types.InlineKeyboardMarkup()
    for i in subcat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'adminsubcat_{i[0]}_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('➕ ' + translater(admin_id, 'Добавить подкатегорию'), callback_data=f'addsubcat_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('📝 ' + translater(admin_id, 'Изменить название'), callback_data=f'changenamecat_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('🗑 ' + translater(admin_id, 'Удалить категорию'), callback_data=f'delcat_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('🔙 ' + translater(admin_id, 'Вернуться'), callback_data='products'))
    return mkp

def get_subcategories_user(cat_id, user_id):
    subcat_list = db.get_subcat(cat_id, user_id)
    mkp = types.InlineKeyboardMarkup()
    for i in subcat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'usersubcat_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('🔙 ' + translater(user_id, 'Вернуться'), callback_data='toshop'))
    return mkp


def get_goods_admin(subcat_id, cat_id, admin_id):
    goods_list = db.get_goods(subcat_id)
    mkp = types.InlineKeyboardMarkup()
    for i in goods_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'admingood_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('➕ ' + translater(admin_id, 'Добавить товар'), callback_data=f'addgood_{subcat_id}_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('📝 ' + translater(admin_id, 'Изменить название'), callback_data=f'changenamesubcat_{subcat_id}'))
    mkp.add(types.InlineKeyboardButton('🗑 ' + translater(admin_id, 'Удалить подкатегорию'), callback_data=f'delsubcat_{subcat_id}'))
    mkp.add(types.InlineKeyboardButton('🔙 ' + translater(admin_id, 'Вернуться'), callback_data=f'admincat_{cat_id}'))
    return mkp

async def send_admin_good(goodid, user_id):
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(user_id, 'Название'), callback_data=f'changegoodname_{goodid}')
    btn2 = types.InlineKeyboardButton(translater(user_id, 'Описание'), callback_data=f'changegooddesc_{goodid}')
    btn3 = types.InlineKeyboardButton(translater(user_id, 'Цену'), callback_data=f'changegoodprice_{goodid}')
    btn4 = types.InlineKeyboardButton('🗑 ' + translater(user_id, 'Удалить'), callback_data=f'delgood_{goodid}')
    btn5 = types.InlineKeyboardButton(translater(user_id, 'Отменить'), callback_data='admin')
    mkp.add(btn1).add(btn2, btn3).add(btn4).add(btn5)
    if good_info[3] == 'None':
        await bot.send_message(user_id, (translater(user_id, 'Название товара:') + f' <code>{good_info[0]}</code>\n' + translater(user_id, 'Описание товара:') + f' <code>{good_info[1]}</code>\n' + translater(user_id, 'Цена:') + f' <code>{good_info[2]}</code>\n\n' + translater(user_id, 'Выберите, что вы хотите изменить')), reply_markup=mkp)
    else:
        await bot.send_photo(user_id, open(f'images/{good_info[3]}', 'rb'), caption=(translater(user_id, 'Название товара:') + f' <code>{good_info[0]}</code>\n' + translater(user_id, 'Описание товара:') + f' <code>{good_info[1]}</code>\n' + translater(user_id, 'Цена:') + f' <code>{good_info[2]}</code>\n\n' + translater(user_id, 'Выберите, что вы хотите изменить')), reply_markup=mkp)


async def send_good(step, subcatid, user_id):
    goods = db.get_goods_user(subcatid, user_id)
    curr = db.get_currencysetadm()[0]

    name = goods[step][1]
    description = goods[step][2]
    price = goods[step][3]
    price = float(price)
    price = f'{price:.2f}'
    photo = goods[step][4]
    goodid = goods[step][0]

    mkp = types.InlineKeyboardMarkup()
    if step == 0:
        btn1 = types.InlineKeyboardButton('❌', callback_data='none')
    else:
        btn1 = types.InlineKeyboardButton('⬅', callback_data=f'catback_{subcatid}_{step-1}')
    btn2 = types.InlineKeyboardButton(f'{step+1}/{len(goods)}', callback_data='none')
    if step+1 == len(goods):
        btn3 = types.InlineKeyboardButton('❌', callback_data='none')
    else:
        btn3 = types.InlineKeyboardButton('➡', callback_data=f'catnext_{subcatid}_{step+1}')
    btn4 = types.InlineKeyboardButton('➖', callback_data='count_min')
    btn5 = types.InlineKeyboardButton('1 '+translater(int(user_id),'шт'), callback_data='none')
    btn6 = types.InlineKeyboardButton('➕', callback_data='count_plus')
    btn7 = types.InlineKeyboardButton(translater(user_id, 'Добавить в корзину'), callback_data=f'tobox_{goodid}')
    btn8 = types.InlineKeyboardButton(translater(user_id, 'В магазин'), callback_data='toshop')
    btn9 = types.InlineKeyboardButton(translater(user_id, 'Корзина'), callback_data='korzina')
    if len(db.get_box(user_id)) == 0:
        mkp.add(btn1, btn2, btn3).add(btn4, btn5, btn6).add(btn7).add(btn8)
    else:
        mkp.add(btn1, btn2, btn3).add(btn4, btn5, btn6).add(btn7).add(btn8).add(btn9)

    if db.check_is_digital(goodid):
        isDigital = '\n——————\n' + translater(user_id, 'Это цифровой товар, он будет сразу отправлен вам после покупки')
    else:
        isDigital = ""
    if photo == 'None':
        await bot.send_message(user_id, '<b>'+translater(user_id, 'Название товара')+f'</b>: <code>{name}</code>\n<b>'+translater(user_id, 'Описание')+f'</b>: {description}\n<b>'+translater(user_id, 'Цена')+f'</b>: <code>{price}</code> {curr}' + isDigital, reply_markup=mkp)
    else:
        await bot.send_photo(user_id, open(f'images/{photo}', 'rb'), caption='<b>'+translater(user_id, 'Название товара')+f'</b>: <code>{name}</code>\n<b>'+translater(user_id, 'Описание')+f'</b>: {description}\n<b>'+translater(user_id, 'Цена')+f'</b>: <code>{price}</code> {curr}' + isDigital, reply_markup=mkp)



async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer(translater(m.from_user.id, "Не флуди"))


def get_courses():
    a = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = a.json()['Valute']['USD']['Value']
    eur = a.json()['Valute']['EUR']['Value']
    returns = [usd, eur]
    return returns

def torub(currency, count):
    a = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = a.json()['Valute']['USD']['Value']
    eur = a.json()['Valute']['EUR']['Value']

    if currency == 'usd':
        returned = float(usd)*float(count)
    elif currency == 'eur':
        returned = float(eur)*float(count)
    else:
        returned = count
    return returned

def rubto(currency, count):
    a = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = a.json()['Valute']['USD']['Value']
    eur = a.json()['Valute']['EUR']['Value']

    if currency == 'usd':
        returned = float(count)/float(usd)
        returned = f'{returned:.2f}'
        returned = float(returned)
    elif currency == 'eur':
        returned = float(count)/float(eur)
        returned = f'{returned:.2f}'
        returned = float(returned)
    else:
        returned = float(count)
        returned = f'{returned:.2f}'
        returned = float(returned)
    return returned

async def update_prices():
    db.update_pricesgood()
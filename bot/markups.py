from aiogram import types
from config import db
from functions import translater


def rules_mkp(user_id):
    mkp = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton('Принять / Accept', callback_data='rulesok')
    btn2 = types.InlineKeyboardButton('Отклонить / Reject', callback_data='rulesno')
    mkp.add(btn1).add(btn2)
    return mkp


def menu_mkp(user_id):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton(translater(user_id, 'Магазин') + " 🛍")
    btn2 = types.KeyboardButton(translater(user_id, 'Меню пользователя') + " 👤")
    btn3 = types.KeyboardButton('❓ F.A.Q. ❓')
    btn4 = types.KeyboardButton(translater(user_id, 'Канал с отзывами') + " 📝")
    btn5 = types.KeyboardButton(translater(user_id, 'Поддержка') + " ✉️")
    mkp.add(btn1, btn2).add(btn5, btn4).add(btn3)
    return mkp

def menu_mkp_without_sprt_btn(user_id):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton(translater(user_id, 'Магазин') + " 🛍")
    btn2 = types.KeyboardButton(translater(user_id, 'Меню пользователя') + " 👤")
    btn3 = types.KeyboardButton('❓ F.A.Q. ❓')
    btn4 = types.KeyboardButton(translater(user_id, 'Канал с отзывами') + " 📝")
    mkp.add(btn1, btn2).add(btn3, btn4)
    return mkp

def menu_mkp_admin(user_id):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton(translater(user_id, 'Магазин') + " 🛍")
    btn2 = types.KeyboardButton(translater(user_id, 'Меню пользователя') + " 👤")
    btn3 = types.KeyboardButton('❓ F.A.Q. ❓')
    btn4 = types.KeyboardButton(translater(user_id, 'Канал с отзывами') + " 📝")
    btn5 = types.KeyboardButton(translater(user_id, 'Поддержка') + " ✉️")
    btn6 = types.KeyboardButton(translater(user_id, 'Админ-панель'))
    mkp.add(btn1, btn2).add(btn5, btn4).add(btn3).add(btn6)
    return mkp

def usermenu_mkp(user_id):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton(translater(user_id, 'Баланс') + " 💰")
    btn2 = types.KeyboardButton(translater(user_id, 'Корзина') + " 🛒")
    btn3 = types.KeyboardButton(translater(user_id, 'Мои покупки') + " 📦")
    btn4 = types.KeyboardButton(translater(user_id, 'Реферальная система') + " 👥")
    btn5 = types.KeyboardButton("⬅️ " + translater(user_id, 'В меню'))
    btn6 = types.KeyboardButton(translater(user_id, 'Изменить язык'))
    if db.check_countlan() == 'ok':
        mkp.add(btn1, btn2).add(btn3, btn4).add(btn5).add(btn6)
    else:
        mkp.add(btn1, btn2).add(btn3, btn4).add(btn5)
    return mkp

def cancel_mkp(user_id):
    mkp = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(translater(user_id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1)
    return mkp

def admin_mkp(user_id):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton(translater(user_id, 'Продукты'))
    btn2 = types.KeyboardButton(translater(user_id, 'Заказы'))
    btn3 = types.KeyboardButton(translater(user_id, 'Пользователи'))
    btn4 = types.KeyboardButton(translater(user_id, 'Заявки на вывод'))
    btn5 = types.KeyboardButton(translater(user_id, 'Настройки бота'))
    btn6 = types.KeyboardButton(translater(user_id, 'Поддержка'))
    btn7 = types.KeyboardButton(translater(user_id, 'Режим покупателя'))
    mkp.add(btn1, btn2).add(btn3, btn4).add(btn5, btn6).add(btn7)
    return mkp

def botsettings_mkp(user_id):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(translater(user_id, 'Платежные системы'))
    btn2 = types.KeyboardButton(translater(user_id, 'Настройка доставки'))
    btn3 = types.KeyboardButton(translater(user_id, 'Изменение реф'))
    btn4 = types.KeyboardButton(translater(user_id, 'Настройка F.A.Q'))
    btn5 = types.KeyboardButton(translater(user_id, 'Изменить правила'))
    btn6 = types.KeyboardButton(translater(user_id, 'Изменить токен бота'))
    btn7 = types.KeyboardButton(translater(user_id, 'Плата за отзыв'))
    btn8 = types.KeyboardButton(translater(user_id, 'Настройка языка'))
    btn9 = types.KeyboardButton(translater(user_id, 'Настройка валют'))
    btn10 = types.KeyboardButton(translater(user_id, 'Назад в админку'))
    mkp.add(btn1, btn2).add(btn3, btn4).add(btn5, btn7).add(btn8, btn9).add(btn10)
    return mkp


def all_users_mkp(page, user_id):
    users_list = db.get_all_users()
    mkp = types.InlineKeyboardMarkup(row_width=2)

    if page == 1:
        if len(users_list) < 11:
            for i in users_list:
                try:
                    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Пользователь') + f' {i[1]} | {db.get_username(int(i[1]))}', callback_data=f'getuser_{i[1]}_{page}'))
                except Exception as ex:
                    print(ex)
        else:
            try:
                for i in range(page-1, page*10):
                    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Пользователь') + f' {users_list[i][1]} | {db.get_username(int(users_list[i][1]))}', callback_data=f'getuser_{users_list[i][1]}_{page}'))
                mkp.add(types.InlineKeyboardButton('Далее', callback_data=f'usersnext_{page+1}'))
            except:
                pass
    else:
        try:
            for i in range((page-1)*10, page*10):
                mkp.add(types.InlineKeyboardButton(translater(user_id, 'Пользователь') + f' {users_list[i][1]} | {db.get_username(int(users_list[i][1]))}', callback_data=f'getuser_{users_list[i][1]}_{page}'))
            mkp.add(types.InlineKeyboardButton(translater(user_id, 'Назад'), callback_data=f'usersback_{page-1}'), types.InlineKeyboardButton(translater(user_id, 'Далее'), callback_data=f'usersnext_{page+1}'))
        except:
            mkp.add(types.InlineKeyboardButton(translater(user_id, 'Назад'), callback_data=f'usersback_{page-1}'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Отменить'), callback_data='admin'))
    return mkp

def deliveriesadm_mkp(user_id):
    delivery_list = db.get_adm_delivery()
    mkp = types.InlineKeyboardMarkup()
    for delivery in delivery_list:
        if delivery[2] == 'off':
            mkp.add(types.InlineKeyboardButton(f'❌ {delivery[1]}', callback_data=f'admdeliveryset_{delivery[0]}'))
        elif delivery[2] == 'on':
            mkp.add(types.InlineKeyboardButton(f'✅ {delivery[1]}', callback_data=f'admdeliveryset_{delivery[0]}'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Добавить доставку'), callback_data='deliveryadd'))
    return mkp

def deliveryuser_mkp(user_id):
    delivery_list = db.get_deliveryuser(int(user_id))
    mkp = types.InlineKeyboardMarkup()
    curr = db.get_currencysetadm()[0]
    for delivery in delivery_list:
        mkp.add(types.InlineKeyboardButton(f'{delivery[1]} | {delivery[2]} {curr.upper()}', callback_data=f'delivery_{delivery[0]}'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Отменить'), callback_data='cancel'))
    return mkp


def questions_mkp(user_id):
    questions_list = db.get_questions()
    mkp = types.InlineKeyboardMarkup()
    for quest in questions_list:
        mkp.add(types.InlineKeyboardButton(translater(user_id, 'Вопрос №') + f'{quest[0]} | {db.get_username(int(quest[1]))}', callback_data=f'question_{quest[0]}'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Вернуться в админ-панель'), callback_data='admin'))
    return mkp

def questions_support_mkp(user_id):
    questions_list = db.get_questions()
    mkp = types.InlineKeyboardMarkup()
    for quest in questions_list:
        mkp.add(types.InlineKeyboardButton(translater(user_id, 'Вопрос №') + f'{quest[0]} | {db.get_username(int(quest[1]))}', callback_data=f'question_{quest[0]}'))
    return mkp

def withdraws_mkp(user_id):
    withdraw_list = db.get_withdraws()
    mkp = types.InlineKeyboardMarkup()
    
    for withdraw in withdraw_list:
        mkp.add(types.InlineKeyboardButton(translater(user_id, 'Заявка №') + f'{withdraw[0]}', callback_data=f'withdr_{withdraw[0]}'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Вернуться в админ-панель'), callback_data='admin'))
    return mkp

def lan_settingmkp(user_id):
    lan_set = db.get_languagesadm()

    mkp = types.InlineKeyboardMarkup()
    if lan_set[0] == 0:
        mkp.add(types.InlineKeyboardButton(translater(user_id, 'Русский') + ' ❌', callback_data='setlanset_ru'))
    else:
        mkp.add(types.InlineKeyboardButton(translater(user_id, 'Русский') + ' ✅', callback_data='setlanset_ru'))
    
    if lan_set[1] == 0:
        mkp.add(types.InlineKeyboardButton(translater(user_id, 'Английский') + ' ❌', callback_data='setlanset_en'))
    else:
        mkp.add(types.InlineKeyboardButton(translater(user_id, 'Английский') + ' ✅', callback_data='setlanset_en'))
    mkp.add(types.InlineKeyboardButton(translater(user_id, 'Админ-панель'), callback_data='admin'))
    return mkp
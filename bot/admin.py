import json
from config import dp, admins, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from markups import admin_mkp, cancel_mkp, all_users_mkp, menu_mkp, menu_mkp_admin, deliveriesadm_mkp, withdraws_mkp, botsettings_mkp, lan_settingmkp
from functions import get_faq_admin, get_categories_admin, get_subcategories_admin, get_goods_admin, send_admin_good, translater
from states import AddSupport, ChangeRef2, NewFaq, FaqName, FaqText, AddCat, AddSubcat, ChangeNamecat, ChangeNamesubcat, AddGood, ChangeNameGood, ChangeDescGood, ChangePriceGood, ChangeRef, OrderEnd, Rassilka, DeliveryAdd, DeliveryChangeName, DeliveryChangeCost, ChangeBalance, GivePromo, GiveSkidka, SendMsg, ChangeStatus, ChangeRules, ChangeToken, ChangeReviewPay, ChageNicknameAdm, AddCatEng, AddCatRus, ChangeNamecatEng, ChangeNamecatRus, AddSubcatEng, AddSubcatRus, ChangeNamesubcatEng, ChangeNamesubcatRus, ChangeNameGoodEng, ChangeNameGoodRus, ChangeDescGoodEng, ChangeDescGoodRus, RassilkaAll
import pickle
import requests

def get_courses():
    a = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = a.json()['Valute']['USD']['Value']
    eur = a.json()['Valute']['EUR']['Value']
    returns = [usd, eur]
    return returns

@dp.message_handler(text='Режим покупателя')
@dp.message_handler(text='Buyer mode')
async def pokupmsg(message: types.Message):
    await message.answer(translater(message.from_user.id, 'Вы перешли в режим покупателя'), reply_markup=menu_mkp_admin(message.from_user.id))


@dp.message_handler(commands='admin')
@dp.message_handler(text='Админ-панель')
@dp.message_handler(text='Admin panel')
@dp.message_handler(text='Назад в админку')
@dp.message_handler(text='Back to admin panel')
@dp.message_handler(text='Go back to the admin panel')
@dp.message_handler(text='Вернуться в админ панель')
@dp.message_handler(text='Вернуться в админ-панель')
@dp.message_handler(text='Return to admin panel')
async def adminCmd(message: types.Message):
    if message.from_user.id in admins:
        db.remove_old_orders()
        await message.answer(translater(message.from_user.id, 'Вы перешли в админ-панель'), reply_markup=admin_mkp(message.from_user.id))


@dp.callback_query_handler(text='admin')
async def adminCall(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer(translater(call.from_user.id, 'Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))

@dp.callback_query_handler(text='cancel',  state=AddSupport.UserId)
async def adminCallFromAddingSupport(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except:
        pass
    try:
        await state.finish()
    except:
        pass
    await call.message.answer(translater(call.from_user.id, 'Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))


@dp.callback_query_handler(text='cancel', state=NewFaq.Name)
@dp.callback_query_handler(text='cancel', state=NewFaq.EngName)
@dp.callback_query_handler(text='cancel', state=NewFaq.Text)
@dp.callback_query_handler(text='cancel', state=NewFaq.EngText)
@dp.callback_query_handler(text='cancel', state=AddSupport.UserId)
@dp.callback_query_handler(text='faqset')
async def faqSetCall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Вы вошли панель редактирования F.A.Q.'), reply_markup=get_faq_admin(call.from_user.id))
    try:
        await state.finish()
    except:
        pass


@dp.message_handler(text='Настройка F.A.Q')
@dp.message_handler(text='Setting F.A.Q')
async def faqSetMsg(message: types.Message):
    await message.answer(translater(message.from_user.id, 'Вы вошли панель редактирования F.A.Q.'), reply_markup=get_faq_admin(message.from_user.id))



@dp.callback_query_handler(text='newfaq')
async def newfaqcall(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    await call.message.answer(translater(call.from_user.id, 'Введите название раздела'), reply_markup=cancel_mkp(call.from_user.id))
    await NewFaq.Name.set()


@dp.message_handler(state=NewFaq.Name)
async def newfaqnamemsg(message: types.Message, state: FSMContext):
    await message.answer(translater(message.from_user.id, 'Хорошо, название будет:') + f' <code>{message.text}</code>')
    async with state.proxy() as data:
        data['Name'] = message.text
    # await message.answer('Введите текст к разделу:', reply_markup=cancel_mkp(message.from_user.id))
    await message.answer(translater(message.from_user.id, 'Введите название на английском'), reply_markup=cancel_mkp(message.from_user.id))
    await NewFaq.next()


@dp.message_handler(state=NewFaq.EngName)
async def newfaqengnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['EngName'] = message.text
    await message.answer(translater(message.from_user.id, 'Введите текст к разделу:'), reply_markup=cancel_mkp(message.from_user.id))
    await NewFaq.next()


@dp.message_handler(state=NewFaq.Text)
async def newfaqtextmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Text'] = message.text
    await message.answer(translater(message.from_user.id, 'Введите текст на английском:'), reply_markup=cancel_mkp(message.from_user.id))
    await NewFaq.next()


@dp.message_handler(state=NewFaq.EngText)
async def newfaqengtextmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['EngText'] = message.text
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Пропустить'), callback_data='skip')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer(translater(message.from_user.id, 'Отправьте фото или нажмите "Пропустить"'), reply_markup=mkp)
    await NewFaq.next()


@dp.callback_query_handler(text='skip', state=NewFaq.Photo)
async def skipnewfawphotocall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        pass
    db.add_faq(data['Name'], data['EngName'], data['Text'], data['EngText'], 'None')
    await call.message.answer(translater(call.from_user.id, 'Успешно добавлено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()


@dp.message_handler(content_types='photo', state=NewFaq.Photo)
async def newfaqphotoctphoto(message: types.message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path.split('/')[-1]
    await bot.download_file(file_info.file_path, f'images/{filename}')
    async with state.proxy() as data:
        data['Photo'] = filename
    db.add_faq(data['Name'], data['EngName'], data['Text'], data['EngText'], filename)
    await message.answer(translater(message.from_user.id, 'Успешно добавлено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='changefaq_')
async def changefaqcall(call: types.CallbackQuery):
    faq_info = db.get_faq_adm(int(call.data.split('_')[1]))
    faqid = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Название'), callback_data=f'changefaqname_{faqid}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Текст'), callback_data=f'changefaqtext_{faqid}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить'), callback_data=f'delfaq_{faqid}')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='faqset')
    mkp.add(btn1, btn2).add(btn3).add(btn4)
    if faq_info[2] == 'None' or faq_info[2] == None:
        await call.message.answer(translater(call.from_user.id, 'Выбран раздел:') + f' <code>{faq_info[0]}</code>\n\n{faq_info[1]}', reply_markup=mkp)
    else:
        await call.message.answer_photo(open(f'images/{faq_info[2]}', 'rb'), caption=(translater(call.from_user.id, 'Выбран раздел:') +f' <code>{faq_info[0]}</code>\n\n{faq_info[1]}'), reply_markup=mkp)


@dp.callback_query_handler(text_contains='changefaqname_')
async def changefaqnamecall(call: types.CallbackQuery, state: FSMContext):
    faqid = call.data.split('_')[1]
    faq_info = db.get_faq_adm(int(faqid))
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Старое название раздела:') + f' <code>{faq_info[0]}</code>\n'+ translater(call.from_user.id, 'Введите новое:'), reply_markup=cancel_mkp(call.from_user.id))
    await FaqName.FaqId.set()
    async with state.proxy() as data:
        data['FaqId'] = faqid


@dp.callback_query_handler(text='cancel', state=FaqName.FaqId)
@dp.callback_query_handler(text='cancel', state=FaqName.Name)
@dp.callback_query_handler(text='cancel', state=FaqText.FaqId)
@dp.callback_query_handler(text='cancel', state=FaqText.Text)
async def faqnamefaqidcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=FaqName.FaqId)
async def faqnamefaqidmsg(message: types.Message, state: FSMContext):
    await FaqName.next()
    async with state.proxy() as data:
        data['Name'] = message.text
    await message.answer(translater(message.from_user.id, 'Введите название на английском'), reply_markup=cancel_mkp(message.from_user.id))


@dp.message_handler(state=FaqName.Name)
async def faqnamenamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    faqid = data['FaqId']
    name = data['Name']
    db.changefaq_name(int(faqid), name, message.text)
    await message.answer(translater(message.from_user.id, 'Название успешно изменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()



@dp.callback_query_handler(text_contains='changefaqtext_')
async def changefaqtextcall(call: types.CallbackQuery, state: FSMContext):
    faqid = call.data.split('_')[1]
    faq_info = db.get_faq_adm(int(faqid))
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Старый текст раздела:') + f' <code>{faq_info[1]}</code>\n' + translater(call.from_user.id, 'Введите новый:'), reply_markup=cancel_mkp(call.from_user.id))
    await FaqText.FaqId.set()
    async with state.proxy() as data:
        data['FaqId'] = faqid


@dp.message_handler(state=FaqText.FaqId)
async def faqtextfaqidmsg(message: types.Message, state: FSMContext):
    await FaqText.next()
    async with state.proxy() as data:
        data['Text'] = message.text
    await message.answer(translater(message.from_user.id, 'Введите текст на английском'), reply_markup=cancel_mkp(message.from_user.id))


@dp.message_handler(state=FaqText.Text)
async def faqtexttextmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    faqid = data['FaqId']
    text = data['Text']
    db.changefaq_text(int(faqid), text, message.text)
    await message.answer(translater(message.from_user.id, 'Текст раздела успешно изменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='delfaq_')
async def delfaqcall(call: types.CallbackQuery):
    faqid = call.data.split('_')[1]
    faq_info = db.get_faq_adm(int(faqid))
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить'), callback_data=f'delfaqq_{faqid}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='faqset')
    mkp.add(btn1).add(btn2)
    await call.message.answer(translater(call.from_user.id, 'Вы действительно хотите удалить раздел') + f' <code>{faq_info[0]}</code>', reply_markup=mkp)


@dp.callback_query_handler(text_contains='delfaqq_')
async def delfaqqcall(call: types.CallbackQuery):
    faqid = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    db.del_faq(int(faqid))
    await call.message.answer(translater(call.from_user.id, 'Раздел успешно удален. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))


@dp.callback_query_handler(text='cancel', state=AddCatRus.CatName)
@dp.callback_query_handler(text='cancel', state=AddCatEng.CatName)
@dp.callback_query_handler(text='cancel', state=AddCat.CatName)
@dp.callback_query_handler(text='cancel', state=AddCat.EngCatName)
@dp.callback_query_handler(text='cancel', state=AddSubcatRus.SubcatName)
@dp.callback_query_handler(text='cancel', state=AddSubcatEng.SubcatName)
@dp.callback_query_handler(text='cancel', state=AddSubcat.SubcatName)
@dp.callback_query_handler(text='cancel', state=AddSubcatRus.SubcatName)
@dp.callback_query_handler(text='cancel', state=AddSubcatEng.SubcatName)
@dp.callback_query_handler(text='cancel', state=AddSubcat.SubcatEngName)
async def orderscall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Выберите категорию/действие:'), reply_markup=get_categories_admin(call.from_user.id))
    try:
        await state.finish()
    except:
        pass


@dp.message_handler(text='Продукты')
@dp.message_handler(text='Products')
async def ordersmsg(message: types.Message):
    await message.answer(translater(message.from_user.id, 'Выберите категорию/действие:'), reply_markup=get_categories_admin(message.from_user.id))


@dp.callback_query_handler(text='products')
async def productscall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Выберите категорию/действие:'), reply_markup=get_categories_admin(call.from_user.id))


@dp.callback_query_handler(text='addcat')
async def addcatcall(call: types.CallbackQuery):
    await call.message.delete()
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название категории:'), reply_markup=cancel_mkp(call.from_user.id))
        await AddCat.CatName.set()
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название категории:'), reply_markup=cancel_mkp(call.from_user.id))
        await AddCatRus.CatName.set()
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название категории на английском:'), reply_markup=cancel_mkp(call.from_user.id))
        await AddCatEng.CatName.set()


@dp.message_handler(state=AddCatRus.CatName)
async def addcatruscatnamemsg(message: types.Message, state: FSMContext):
    db.add_cat(message.text, 'None')
    await message.answer(translater(message.from_user.id, 'Категория успешно добавлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=AddCatEng.CatName)
async def addcatruscatnamemsg(message: types.Message, state: FSMContext):
    db.add_cat('None', message.text)
    await message.answer(translater(message.from_user.id, 'Категория успешно добавлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=AddCat.CatName)
async def addcatcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['CatName'] = message.text
    await message.answer(translater(message.from_user.id, 'Введите название категории на английском:'), reply_markup=cancel_mkp(message.from_user.id))
    await AddCat.next()


@dp.message_handler(state=AddCat.EngCatName)
async def addcatengcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    catname = data['CatName']
    db.add_cat(catname, message.text)
    await message.answer(translater(message.from_user.id, 'Категория успешно добавлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecat.CatId)
@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecatRus.CatId)
@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecatEng.CatId)
@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecatRus.CatName)
@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecatEng.CatName)
@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecat.CatName)
@dp.callback_query_handler(text_contains='admincat_')
async def admincatcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    cat_id = call.data.split('_')[1]
    cat_name = db.get_cat_name(int(cat_id))
    await call.message.answer(translater(call.from_user.id, 'Категория:') + f' <code>{cat_name}</code>\n' + translater(call.from_user.id, 'Выберите, подкатегорию/действие:'), reply_markup=get_subcategories_admin(int(cat_id), call.from_user.id))
    try:
        await state.finish()
    except:
        pass


@dp.callback_query_handler(text_contains='addsubcat_')
async def addsubcatcall(call: types.CallbackQuery, state: FSMContext):
    cat_id = call.data.split('_')[1]
    await call.message.delete()
    check_lan = db.check_lanadd()
    print(check_lan)
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название подкатегории:'), reply_markup=cancel_mkp(call.from_user.id))
        await AddSubcat.CatId.set()
        async with state.proxy() as data:
            data['CatId'] = cat_id
        await AddSubcat.next()
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название подкатегории:'), reply_markup=cancel_mkp(call.from_user.id))
        await AddSubcatRus.CatId.set()
        async with state.proxy() as data:
            data['CatId'] = cat_id
        await AddSubcatRus.next()
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название подкатегории на английском:'), reply_markup=cancel_mkp(call.from_user.id))
        await AddSubcatEng.CatId.set()
        async with state.proxy() as data:
            data['CatId'] = cat_id
        await AddSubcatEng.next()
    



@dp.message_handler(state=AddSubcat.SubcatName)
async def addsubcatsubcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['SubcatName'] = message.text
    # db.add_subcat(int(cat_id), message.text)
    # await message.answer('Подкатегория успешно добавлена! Вы были возвращены в админ-панель', reply_markup=admin_mkp(message.from_user.id))
    await message.answer(translater(message.from_user.id, 'Введите название подкатегории на английском:'), reply_markup=cancel_mkp(message.from_user.id))
    await AddSubcat.next()


@dp.message_handler(state=AddSubcatRus.SubcatName)
async def addsubcatrussubcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    print('here')
    catid = data['CatId']
    db.add_subcat(int(catid), message.text, 'None')
    await message.answer(translater(message.from_user.id, 'Подкатегория успешно добавлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=AddSubcatEng.SubcatName)
async def addsubcatengsubcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    catid = data['CatId']
    db.add_subcat(int(catid), 'None', message.text)
    await message.answer(translater(message.from_user.id, 'Подкатегория успешно добавлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=AddSubcat.SubcatEngName)
async def addsubcatengnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    catid = data['CatId']
    subcatname = data['SubcatName']
    db.add_subcat(int(catid), subcatname, message.text)
    await message.answer(translater(message.from_user.id, 'Подкатегория успешно добавлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()



@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Name)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.EngName)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Description)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.EngDescription)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Photo)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Price)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcat.SubcatId)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcatRus.SubcatId)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcatEng.SubcatId)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcat.SubcatName)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcatRus.SubcatName)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcatEng.SubcatName)
@dp.callback_query_handler(text_contains='adminsubcat_')
async def adminsubcatcall(call: types.CallbackQuery, state: FSMContext):
    subcat_id = call.data.split('_')[1]
    cat_id = call.data.split('_')[2]
    subcat_name = db.get_subcat_name(int(subcat_id))
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Подкатегория:') + f' <code>{subcat_name}</code>\n' + translater(call.from_user.id, 'Выберите товар/действие:'), reply_markup=get_goods_admin(int(subcat_id), cat_id, call.from_user.id))
    try:
        await state.finish()
    except:
        pass


@dp.callback_query_handler(text_contains='changenamecat_')
async def changenamecatcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    cat_id = call.data.split('_')[1]
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Вернуться'), callback_data=f'admincat_{cat_id}')
    mkp.add(btn1)
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название категории:'), reply_markup=mkp)
        await ChangeNamecat.CatId.set()
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название категории:'), reply_markup=mkp)
        await ChangeNamecatRus.CatId.set()
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название категории на английском:'), reply_markup=mkp)
        await ChangeNamecatEng.CatId.set()
    async with state.proxy() as data:
        data['CatId'] = cat_id


@dp.message_handler(state=ChangeNamecat.CatId)
async def changenamecatcatidmsg(message: types.Message, state: FSMContext):
    await ChangeNamecat.next()
    async with state.proxy() as data:
        data['CatName'] = message.text
    cat_id = data['CatId']
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Вернуться'), callback_data=f'admincat_{cat_id}')
    mkp.add(btn1)
    # db.changename_cat(int(cat_id), message.text)
    # await message.answer('Название категории успешно изменено! Вы были возвращены в админ-панель', reply_markup=admin_mkp(message.from_user.id))
    await message.answer(translater(message.from_user.id, 'Введите название категории на английском:'), reply_markup=mkp)


@dp.message_handler(state=ChangeNamecatEng.CatId)
async def changenamecatengcatidmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    cat_id = data['CatId']
    db.changename_cat(int(cat_id), 'None', message.text)
    await message.answer(translater(message.from_user.id, 'Название категории успешно изменено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=ChangeNamecatRus.CatId)
async def changenamecatruscatidmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    cat_id = data['CatId']
    db.changename_cat(int(cat_id), message.text, 'None')
    await message.answer(translater(message.from_user.id, 'Название категории успешно изменено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=ChangeNamecat.CatName)
async def changenamecatcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    cat_id = data['CatId']
    catname = data['CatName']
    db.changename_cat(int(cat_id), catname, message.text)
    await message.answer(translater(message.from_user.id, 'Название категории успешно изменено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='changenamesubcat_')
async def changenamesubcatcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    subcat_id = call.data.split('_')[1]
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Вернуться'), callback_data=f'adminsubcat_{subcat_id}')
    mkp.add(btn1)
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название подкатегории:'), reply_markup=mkp)
        await ChangeNamesubcat.SubcatId.set()
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название подкатегории:'), reply_markup=mkp)
        await ChangeNamesubcatRus.SubcatId.set()
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название подкатегории на английском:'), reply_markup=mkp)
        await ChangeNamesubcatEng.SubcatId.set()
    async with state.proxy() as data:
        data['SubcatId'] = subcat_id


@dp.message_handler(state=ChangeNamesubcat.SubcatId)
async def changenamesubcatsubcatidmsg(message: types.Message, state: FSMContext):
    await ChangeNamesubcat.next()
    async with state.proxy() as data:
        data['SubcatName'] = message.text
    # subcat_id = data['SubcatId']
    # db.changename_subcat(int(subcat_id), message.text)
    # await message.answer('Название подкатегории успешно изменено! Вы были возвращены в админ-панель', reply_markup=admin_mkp(message.from_user.id))
    # await state.finish()
    await message.answer(translater(message.from_user.id, 'Введите название подкатегории на английском языке'), reply_markup=cancel_mkp(message.from_user.id))


@dp.message_handler(state=ChangeNamesubcatEng.SubcatId)
async def changenamesubcatengmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    subcatid = data['SubcatId']
    db.changename_subcat(int(subcatid), 'None', message.text)
    await message.answer(translater(message.from_user.id, 'Название подкатегории успешно изменено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=ChangeNamesubcatRus.SubcatId)
async def changenamesubcatrusmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    subcatid = data['SubcatId']
    db.changename_subcat(int(subcatid), message.text, 'None')
    await message.answer(translater(message.from_user.id, 'Название подкатегории успешно изменено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.message_handler(state=ChangeNamesubcat.SubcatName)
async def changenamesubncatsubcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    subcatid = data['SubcatId']
    subcatname = data['SubcatName']
    db.changename_subcat(int(subcatid), subcatname, message.text)
    await message.answer(translater(message.from_user.id, 'Название подкатегории успешно изменено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='addgood_')
async def addgoodcall(call: types.CallbackQuery, state: FSMContext):
    subcatid = call.data.split('_')[1]
    cat_id = call.data.split('_')[2]
    await AddGood.SubcatId.set()
    await AddGood.CatId.set()
    async with state.proxy() as data:
        data['SubcatId'] = subcatid
        data['CatId'] = cat_id
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название товара:'), reply_markup=mkp)
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название товара:'), reply_markup=mkp)
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название на английском:'), reply_markup=mkp)
    await AddGood.next()


@dp.message_handler(state=AddGood.Name)
async def addgoodnamemsg(message: types.Message, state: FSMContext):
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        async with state.proxy() as data:
            data['Name'] = message.text
        subcatid = data['SubcatId']
        cat_id = data['CatId']        
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1)
        await message.answer(translater(message.from_user.id, 'Введите название товара на английском:'), reply_markup=mkp)
        # await message.answer('Введите описание к товару:', reply_markup=mkp)
        await AddGood.next()
    elif check_lan[0] == 1:
        async with state.proxy() as data:
            data['Name'] = message.text
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1)
        await message.answer(translater(message.from_user.id, 'Введите описание к товару:'), reply_markup=mkp)
        await AddGood.next()
        async with state.proxy() as data:
            data['EngName'] = 'None'
        await AddGood.next()
    elif check_lan[1] == 1:
        async with state.proxy() as data:
            data['Name'] = 'None'
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        await AddGood.next()
        async with state.proxy() as data:
            data['EngName'] = message.text
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1)
        await message.answer(translater(message.from_user.id, 'Введите описание к товару на английском:'), reply_markup=mkp)
        await AddGood.next()
        await AddGood.next()


@dp.message_handler(state=AddGood.EngName)
async def addgoodengnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['EngName'] = message.text
    subcatid = data['SubcatId']
    cat_id = data['CatId'] 
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    await message.answer(translater(message.from_user.id, 'Введите описание к товару:'), reply_markup=mkp)
    await AddGood.next()

@dp.message_handler(state=AddGood.Description)
async def addgooddescriptionmsg(message: types.Message, state: FSMContext):
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        async with state.proxy() as data:
            data['Description'] = message.text
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1)

        await message.answer(translater(message.from_user.id, 'Введите описание к товару на английском:'), reply_markup=mkp)
        await AddGood.next()
    elif check_lan[0] == 1:
        async with state.proxy() as data:
            data['Description'] = message.text
        subcatid = data['SubcatId']
        cat_id = data['CatId']
        await AddGood.next()
        async with state.proxy() as data:
            data['EngDescription'] = 'None'
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Пропустить'), callback_data='skip')
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1).add(btn2)
        await message.answer(translater(message.from_user.id, 'Отправьте фото или нажмите "Пропустить"'), reply_markup=mkp)
        await AddGood.next()
    elif check_lan[1] == 1:
        async with state.proxy() as data:
            data['Description'] = 'None'
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        await AddGood.next()
        async with state.proxy() as data:
            data['EngDescription'] = message.text
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Пропустить'), callback_data='skip')
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1).add(btn2)
        await message.answer(translater(message.from_user.id, 'Отправьте фото или нажмите "Пропустить"'), reply_markup=mkp)
        await AddGood.next()
        
        

@dp.message_handler(state=AddGood.EngDescription)
async def addgoodengdescmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['EngDescription'] = message.text
    subcatid = data['SubcatId']
    cat_id = data['CatId'] 
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Пропустить'), callback_data='skip')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1).add(btn2)
    await message.answer(translater(message.from_user.id, 'Отправьте фото или нажмите "Пропустить"'), reply_markup=mkp)
    await AddGood.next()

@dp.message_handler(content_types='photo', state=AddGood.Photo)
async def addgoodphotophoto(message: types.Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path.split('/')[-1]
    await bot.download_file(file_info.file_path, f'images/{filename}')
    async with state.proxy() as data:
        data['Photo'] = filename
    subcatid = data['SubcatId']
    cat_id = data['CatId'] 
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    await message.answer(translater(message.from_user.id, 'Введите цену (целым числом, либо через точку, например: <code>249.50</code>)'), reply_markup=mkp)
    await AddGood.next()

@dp.callback_query_handler(text='skip', state=AddGood.Photo)
async def addgoodphotoskipcall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['Photo'] = 'None'
    subcatid = data['SubcatId']
    cat_id = data['CatId'] 
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    await call.message.delete_reply_markup()
    await call.message.answer(translater(call.from_user.id, 'Введите цену (целым числом, либо через точку, например: <code>249.50</code>)'), reply_markup=mkp)
    await AddGood.next()


@dp.message_handler(state=AddGood.Price)
async def addgoodprice(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        async with state.proxy() as data:
            data['Price'] = price
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        name = data['Name']
        engname = data['EngName']
        description = data['Description']
        engdesc = data['EngDescription']
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Добавить'), callback_data='add')
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1).add(btn2)
        if name != 'None' and engname != 'None':
            # await message.answer(f'Name: {engname}\nDescription: {engdesc}')
            if data['Photo'] == 'None':
                await message.answer((translater(message.from_user.id, 'Название товара:') + f' <code>{name}</code>\n' + translater(message.from_user.id, 'Описание:') + f' <code>{description}</code>\n' + translater(message.from_user.id, 'Цена:') + f' <code>{price}</code>'), reply_markup=mkp)
            else:
                photo = data['Photo']
                await message.answer_photo(open(f'images/{photo}', 'rb'), caption=(translater(message.from_user.id, 'Название товара:') + f' <code>{name}</code>\n' + translater(message.from_user.id, 'Описание:') + f' <code>{description}</code>\n' + translater(message.from_user.id, 'Цена:') + f' <code>{price}</code>'), reply_markup=mkp)
        elif name !=  'None':
            if data['Photo'] == 'None':
                await message.answer((translater(message.from_user.id, 'Название товара:') + f' <code>{name}</code>\n' + translater(message.from_user.id, 'Описание:') + f' <code>{description}</code>\n' + translater(message.from_user.id, 'Цена:') + f' <code>{price}</code>'), reply_markup=mkp)
            else:
                photo = data['Photo']
                await message.answer_photo(open(f'images/{photo}', 'rb'), caption=(translater(message.from_user.id, 'Название товара:') + f' <code>{name}</code>\n' + translater(message.from_user.id, 'Описание:') + f' <code>{description}</code>\n' + translater(message.from_user.id, 'Цена:') + f' <code>{price}</code>'), reply_markup=mkp)
        elif name == 'None':
            if data['Photo'] == 'None':
                await message.answer((translater(message.from_user.id, 'Название товара:') + f' <code>{name}</code>\n' + translater(message.from_user.id, 'Описание:') + f' <code>{description}</code>\n' + translater(message.from_user.id, 'Цена:') + f' <code>{price}</code>'), reply_markup=mkp)
            else:
                photo = data['Photo']
                await message.answer_photo(open(f'images/{photo}', 'rb'), caption=(translater(message.from_user.id, 'Название товара:') + f' <code>{name}</code>\n' + translater(message.from_user.id, 'Описание:') + f' <code>{description}</code>\n' + translater(message.from_user.id, 'Цена:') + f' <code>{price}</code>'), reply_markup=mkp)
    except Exception as ex:
        print(ex)
        async with state.proxy() as data:
            pass
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1)
        await message.answer(translater(message.from_user.id, 'Вы неправильно ввели цену! Введите цену целым числом, либо через точку, например: <code>249.50</code>'))

@dp.callback_query_handler(text='add', state=AddGood.Price)
async def addgoodpricecalladd(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    subcat_id = data['SubcatId']
    name = data['Name']
    engname = data['EngName']
    description = data['Description']
    engdesc = data['EngDescription']
    photo = data['Photo']
    price = data['Price']
    currency = db.get_currencysetadm()[0]
    db.add_good(subcat_id, name, engname, description, engdesc, photo, price, currency)
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Товар был успешно добавлен! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='admingood_', state=ChangePriceGood.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGood.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGoodRus.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGoodEng.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGoodRus.GoodDesc)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGoodEng.GoodDesc)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGood.GoodDesc)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGood.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGoodRus.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGoodEng.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGood.GoodName)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGoodRus.GoodName)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGoodEng.GoodName)
@dp.callback_query_handler(text_contains='admingood_')
async def admingoodcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Название'), callback_data=f'changegoodname_{goodid}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Описание'), callback_data=f'changegooddesc_{goodid}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Цену'), callback_data=f'changegoodprice_{goodid}')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить'), callback_data=f'delgood_{goodid}')
    btn5 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='admin')
    mkp.add(btn1).add(btn2, btn3).add(btn4).add(btn5)
    if good_info[3] == 'None':
        await call.message.answer(translater(call.from_user.id, 'Название товара:') + f' <code>{good_info[0]}</code>\n' + translater(call.from_user.id, 'Описание товара:') + f' <code>{good_info[1]}</code>\n' + translater(call.from_user.id, 'Цена:') + f' <code>{good_info[2]}</code>\n\n' + translater(call.from_user.id, 'Выберите, что вы хотите изменить'), reply_markup=mkp)
    else:
        await call.message.answer_photo(open(f'images/{good_info[3]}', 'rb'), caption=(translater(call.from_user.id, 'Название товара:') + f' <code>{good_info[0]}</code>\n' + translater(call.from_user.id, 'Описание товара:') + f' <code>{good_info[1]}</code>\n' + translater(call.from_user.id, 'Цена:') + f' <code>{good_info[2]}</code>\n\n' + translater(call.from_user.id, 'Выберите, что вы хотите изменить')), reply_markup=mkp)
    try:
        await state.finish()
    except:
        pass


@dp.callback_query_handler(text_contains='changegoodname_')
async def changegoodnamecall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Вернуться'), callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название для товара') + f' <code>{good_info[0]}</code>', reply_markup=mkp)
        await ChangeNameGood.GoodId.set()
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название для товара') + f' <code>{good_info[0]}</code>', reply_markup=mkp)
        await ChangeNameGoodRus.GoodId.set()
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое название на английском для товара') + f' <code>{good_info[0]}</code>', reply_markup=mkp)
        await ChangeNameGoodEng.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodid
    

@dp.message_handler(state=ChangeNameGood.GoodId)
async def changenamegoodgoodidmsg(message: types.Message, state: FSMContext):
    await ChangeNameGood.next()
    async with state.proxy() as data:
        data['GoodName'] = message.text
    goodid = data['GoodId']
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Вернуться'), callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    await message.answer(translater(message.from_user.id, 'Введите новое название товара на английском:'), reply_markup=mkp)

@dp.message_handler(state=ChangeNameGoodEng.GoodId)
async def changenamegoodengmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    db.change_namegood(int(goodid), 'None', message.text)
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()

@dp.message_handler(state=ChangeNameGoodRus.GoodId)
async def changenamegoodrusmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    db.change_namegood(int(goodid), message.text, 'None')
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()

@dp.message_handler(state=ChangeNameGood.GoodName)
async def changenamegoodnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    goodname = data['GoodName']
    db.change_namegood(int(goodid), goodname, message.text)
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()

@dp.callback_query_handler(text_contains='changegooddesc_')
async def changegooddesccall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Вернуться'), callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое описание для товара') + f' <code>{good_info[0]}</code>', reply_markup=mkp)
        await ChangeDescGood.GoodId.set()
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое описание для товара') + f' <code>{good_info[0]}</code>', reply_markup=mkp)
        await ChangeDescGoodRus.GoodId.set()
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите новое описание на английском для товара') + f' <code>{good_info[0]}</code>', reply_markup=mkp)
        await ChangeDescGoodEng.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodid


@dp.message_handler(state=ChangeDescGood.GoodId)
async def changedescgoodgoodidmsg(message: types.Message, state: FSMContext):
    await ChangeDescGood.next()
    async with state.proxy() as data:
        data['GoodDesc'] = message.text
    goodid = data['GoodId']
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Вернуться'), callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    await message.answer(translater(message.from_user.id, 'Введите описание на английском:'), reply_markup=mkp)


@dp.message_handler(state=ChangeDescGoodEng.GoodId)
async def changedescgoodengmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    db.change_descgood(int(goodid), 'None', message.text)
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()

@dp.message_handler(state=ChangeDescGoodRus.GoodId)
async def changedescgoodrusmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    db.change_descgood(int(goodid), message.text, 'None')
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()


@dp.message_handler(state=ChangeDescGood.GoodDesc)
async def changedescgooddescmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    gooddesc = data['GoodDesc']
    db.change_descgood(int(goodid), gooddesc, message.text)
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()



@dp.callback_query_handler(text_contains='changegoodprice_')
async def changegoodpricecall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Вернуться'), callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    await call.message.answer(translater(call.from_user.id, 'Введите новую цену для товара') + f' <code>{good_info[0]}</code>', reply_markup=mkp)
    await ChangePriceGood.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodid

@dp.message_handler(state=ChangePriceGood.GoodId)
async def changepricegoodgoodidmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    try:
        price = float(message.text)
        currency = db.get_currencysetadm()[0]
        db.change_pricegood(int(goodid), price, currency)
        await send_admin_good(int(goodid), message.from_user.id)
        await state.finish()
    except:
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Вернуться'), callback_data=f'admingood_{goodid}')
        mkp.add(btn1)
        await message.answer(translater(message.from_user.id, 'Введите цену целым числом, либо через точку, например <code>149.50</code>'), reply_markup=mkp)

@dp.callback_query_handler(text_contains='delgood_')
async def delgoodcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить'), callback_data=f'delgoodd_{goodid}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data=f'admingood_{goodid}')
    mkp.add(btn1, btn2)
    await call.message.answer(translater(call.from_user.id, 'Вы действительно хотите удалить товар') + f' <code>{good_info[0]}</code>?', reply_markup=mkp)


@dp.callback_query_handler(text_contains='delgoodd_')
async def delgooddcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    db.del_good(int(goodid))
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Товар успешно удален! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))

@dp.callback_query_handler(text_contains='delcat_')
async def delcatcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    catname = db.get_namecat(int(catid))
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить'), callback_data=f'delcatt_{catid}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='admin')
    mkp.add(btn1, btn2)
    await call.message.answer(translater(call.from_user.id, 'Вы действительно хотите удалить категорию') + f' <code>{catname}</code>?', reply_markup=mkp)


@dp.callback_query_handler(text_contains='delcatt_')
async def delcattcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    db.del_cat(int(catid))
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Категория успешно удалена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))


@dp.callback_query_handler(text_contains='delsubcat_')
async def delsubcatcall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    subcatname = db.get_namesubcat(int(subcatid))
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить'), callback_data=f'delsubcatt_{subcatid}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='admin')
    mkp.add(btn1, btn2)
    await call.message.answer(translater(call.from_user.id, 'Вы действительно хотите удалить подкатегорию') + f' <code>{subcatname}</code>?', reply_markup=mkp)

@dp.callback_query_handler(text_contains='delsubcatt_')
async def delsubcattcall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    await call.message.delete()
    db.del_subcat(int(subcatid))
    await call.message.answer(translater(call.from_user.id, 'Подкатегория успешно удалена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))



@dp.message_handler(text='Изменение реф')
@dp.message_handler(text='Change ref')
async def changerefmsg(message: types.Message):
    ref = db.get_refproc()
    await message.answer(translater(message.from_user.id, 'Действующий процент с реф системы:') + f' <code>{ref}</code>\n' + translater(message.from_user.id, 'Введите новый'), reply_markup=cancel_mkp(message.from_user.id))
    await ChangeRef.Ref.set()

@dp.callback_query_handler(state=ChangeRef.Ref, text='cancel')
async def cancelchangerefrefcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=ChangeRef.Ref)
async def changerefrefmsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        db.change_ref(message.text)
        await message.answer(translater(message.from_user.id, 'Процент с реф системы успешно изменен! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
        await state.finish()
    else:
        await message.answer(translater(message.from_user.id, 'Введите процент целым числом, либо нажмите "Отменить"'), reply_markup=cancel_mkp(message.from_user.id))

@dp.message_handler(text='Заказы')
@dp.message_handler(text='Orders')
async def ordersmsg(message: types.Message):
    orders = db.get_all_activeorders()
    if len(orders) == 0:
        await message.answer(translater(message.from_user.id, 'Активных заказов не обнаружено'))
    else:
        mkp = types.InlineKeyboardMarkup()
        for i in orders:
            mkp.add(types.InlineKeyboardButton(translater(message.from_user.id, 'Активный заказ №') + f'{i[0]}', callback_data=f'orderadmin_{i[0]}'))
        await message.answer(translater(message.from_user.id, 'Список активных заказов:'), reply_markup=mkp)




@dp.callback_query_handler(text_contains='orderadmin_')
async def orderadmincall(call: types.CallbackQuery):
    order_id = call.data.split('_')[1]
    await call.message.delete()
    order_info = db.get_order_info(int(order_id))
    tovars = pickle.loads(order_info[0])
    adress = order_info[1]
    comment = order_info[2]
    photo = order_info[3]
    catAndSudcatDict = json.loads(order_info[4])
    user_id = db.get_order_userid(int(order_id))
    usernamerev = db.get_usernamerev(int(user_id))
    username = db.get_username(int(user_id))

    text = f'{usernamerev} / {user_id} / {username}\n'

    for i in catAndSudcatDict:
        text += f'{i}\n'
        for j in catAndSudcatDict[i]:
            text += f'     {j}\n'
            num = 1
            for k in catAndSudcatDict[i][j]:
                text += f'          {num}) {db.get_good_info(k, call.from_user.id)[0]}\n'
                num += 1

    text += f'Сумма: {round(float(tovars[-1]), 2)}\n'
    text += f'\n{adress}\n' + translater(call.from_user.id, 'Комментарий:') + f' <code>{comment}</code>'
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Подтвердить'), callback_data=f'orderok_{order_id}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отклонить'), callback_data=f'orderno_{order_id}')
    mkp.add(btn1).add(btn2)
    await call.message.answer(text, reply_markup=mkp)

@dp.callback_query_handler(text_contains='orderno_')
async def ordernocall(call: types.CallbackQuery):
    order_id = call.data.split('_')[1]
    await call.message.delete()
    user_id = db.get_order_userid(int(order_id))
    db.order_cancel(int(order_id), int(user_id))
    p = db.get_order_price(int(order_id))[-1]
    try:
        db.add_balance(int(user_id), float(p))
        await bot.send_message(int(user_id), translater(call.from_user.id, 'Менеджер отклонил заказ. Свяжитесь с ним для подробностей: @') + f'{call.from_user.username}')
        await call.message.answer(translater(call.from_user.id, 'Клиент получил уведомление и ваш username для связи'))
    except:
        await call.message.answer(translater(call.from_user.id, 'Клиент заблокировал бота'))


@dp.callback_query_handler(text_contains='orderok_')
async def orderokcall(call: types.CallbackQuery, state: FSMContext):
    order_id = call.data.split('_')[1]
    await OrderEnd.OrderId.set()
    async with state.proxy() as data:
        data['OrderId'] = order_id
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Подтвердить'), callback_data='ok')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await call.message.answer(translater(call.from_user.id, 'Отправьте фотографию чека и трек кода. ВНИМАНИЕ, все сообщения, что вы напишите - сразу получит пользователь'), reply_markup=mkp)

@dp.callback_query_handler(text='cancel', state=OrderEnd.OrderId)
async def cancelorderendorderidcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()


@dp.message_handler(state=OrderEnd.OrderId, content_types='photo')
async def orderendorderidphoto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    order_id = data['OrderId']
    user_id = db.get_order_userid(int(order_id))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Подтвердить'), callback_data='ok')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)
    try:
        await bot.send_photo(int(user_id), message.photo[-1].file_id, caption=f'Менеджер отправил фото трек кода и чека по заказу №{order_id}')
        await message.answer(translater(message.from_user.id, 'Пользователь получил фотографию. Отправьте ещё сообщение или нажмите "Подтвердить"'), reply_markup=mkp)
    except:
        await message.answer(translater(message.from_user.id, 'Пользователь заблокировал бота. Заказ перешел в завершенный'))
        db.order_end(int(order_id))
        await message.answer(translater(message.from_user.id, 'Вы в админ-панели'), reply_markup=admin_mkp(message.from_user.id))
        await state.finish()

@dp.callback_query_handler(text='ok', state=OrderEnd.OrderId)
async def orderendorderidokcall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    order_id = data['OrderId']
    user_id = db.get_order_userid(int(order_id))
    await bot.send_message(int(user_id), translater(int(user_id), 'По желанию, вы можете оставить отзыв'), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(translater(int(user_id), 'Оставить отзыв'), callback_data=f'takeotziv_{order_id}')))
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Заказ перешел в завершенный'))
    db.order_end(int(order_id))
    await call.message.answer(translater(call.from_user.id, 'Вы в админ-панели'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=OrderEnd.OrderId)
async def orderendorderidmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    order_id = data['OrderId']
    user_id = db.get_order_userid(int(order_id))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Подтвердить'), callback_data='ok')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)
    try:
        await bot.send_message(int(user_id), f'{message.text}')
        await message.answer(translater(message.from_user.id, 'Пользователь получил сообщение. Отправьте ещё или нажмите "Подтвердить"'), reply_markup=mkp)
    except:
        await message.answer(translater(message.from_user.id, 'Пользователь заблокировал бота. Заказ перешел в завершенный'))
        db.order_end(int(order_id))
        await message.answer(translater(message.from_user.id, 'Вы в админ-панели'), reply_markup=admin_mkp(message.from_user.id))
        await state.finish()

@dp.message_handler(text='Пользователи')
@dp.message_handler(text='Users')
async def usersmsg(message: types.Message):
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Рассылка покупателям'), callback_data='rassilka')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Рассылка всем'), callback_data='rassilkaall')
    btn3 = types.InlineKeyboardButton(translater(message.from_user.id, 'Список пользователей'), callback_data='userslist')
    mkp.add(btn1).add(btn2).add(btn3)
    await message.answer(translater(message.from_user.id, 'Выберите действие'), reply_markup=mkp)

@dp.callback_query_handler(text='rassilkaall')
async def rassilkaallcall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Введите сообщение для рассылки:'), reply_markup=cancel_mkp(call.from_user.id))
    await RassilkaAll.List.set()

@dp.message_handler(content_types=['text', 'photo', 'video'], state=RassilkaAll.List)
async def rassilkaalltextmsg(message: types.Message, state: FSMContext):
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отправить'), callback_data='go')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)

    if message.photo:
        await bot.send_photo(message.from_user.id, message.photo[-1].file_id, caption=message.caption, parse_mode="html")
        async with state.proxy() as data:
            data['List'] = {"type": "photo", "msg_id": int(message.message_id), "text": message.caption}
            
    elif message.video:
        await bot.send_video(message.from_user.id, message.video.file_id, caption=message.caption, parse_mode="html")
        async with state.proxy() as data:
            data['List'] = {"type": "video", "msg_id": int(message.message_id), "text": message.caption}

    elif message.text:
        await bot.send_message(message.from_user.id, f'{message.text}', parse_mode="html")
        async with state.proxy() as data:
            data['List'] = {"type": "text", "msg_id": int(message.message_id), "text": message.text}

    await message.answer(translater(message.from_user.id, f'Вы хотите отправить сообщение выше всем пользователям?'), reply_markup=mkp)

@dp.callback_query_handler(text='go', state=RassilkaAll.List)
async def gorassilkaalltextcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer(translater(call.from_user.id, 'Рассылка началась!'))
    await call.message.answer(translater(call.from_user.id, 'Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    async with state.proxy() as data:
        pass
    paramList = data['List']
    await state.finish()

    msgType = paramList["type"]
    msg_id = paramList["msg_id"]
    text = paramList["text"]

    users = db.get_all_users()
    for user in users:
        try:
            await bot.copy_message(user[1], call.from_user.id, msg_id)            
        except:
            pass
    await call.message.answer(translater(call.from_user.id, 'Рассылка завершена!'))

@dp.callback_query_handler(text='rassilka')
async def rassilkacall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Введите сообщение для рассылки:'), reply_markup=cancel_mkp(call.from_user.id))
    await Rassilka.List.set()

@dp.callback_query_handler(text='cancel', state=Rassilka.List)
@dp.callback_query_handler(text='cancel', state=RassilkaAll.List)
async def cancelrassilkatextcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=Rassilka.List)
async def rassilkatextmsg(message: types.Message, state: FSMContext):
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отправить'), callback_data='go')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)

    if message.photo:
        await bot.send_photo(message.from_user.id, message.photo[-1].file_id, caption=message.caption, parse_mode="html")
        async with state.proxy() as data:
            data['List'] = {"type": "photo", "msg_id": int(message.message_id), "text": message.caption}
            
    elif message.video:
        await bot.send_video(message.from_user.id, message.video.file_id, caption=message.caption, parse_mode="html")
        async with state.proxy() as data:
            data['List'] = {"type": "video", "msg_id": int(message.message_id), "text": message.caption}

    elif message.text:
        await bot.send_message(message.from_user.id, f'{message.text}', parse_mode="html")
        async with state.proxy() as data:
            data['List'] = {"type": "text", "msg_id": int(message.message_id), "text": message.text}

    await message.answer(translater(message.from_user.id, f'Вы хотите отправить сообщение выше всем пользователям?'), reply_markup=mkp)

@dp.callback_query_handler(text='go', state=Rassilka.List)
async def gorassilkatextcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer(translater(call.from_user.id, 'Рассылка началась!'))
    await call.message.answer(translater(call.from_user.id, 'Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    async with state.proxy() as data:
        pass
    paramList = data['List']
    await state.finish()

    msgType = paramList["type"]
    msg_id = paramList["msg_id"]
    text = paramList["text"]
    users = db.get_users_pay()
    for user in users:
        try:
            await bot.copy_message(user[1], call.from_user.id, msg_id)
        except:
            pass
    await call.message.answer(translater(call.from_user.id, 'Рассылка завершена!'))

@dp.callback_query_handler(text='userslist')
async def userslistcall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Страница') + ' №1', reply_markup=all_users_mkp(1, call.from_user.id))

@dp.callback_query_handler(text_contains='usersnext_')
async def usersnextcall(call: types.CallbackQuery):
    page = call.data.split('_')[1]
    await call.message.edit_text(translater(call.from_user.id, 'Страница') + f' №{page}', reply_markup=all_users_mkp(int(page), call.from_user.id))

@dp.callback_query_handler(text_contains='usersback_')
async def usersnextcall(call: types.CallbackQuery):
    page = call.data.split('_')[1]
    await call.message.edit_text(translater(call.from_user.id, 'Страница') + f' №{page}', reply_markup=all_users_mkp(int(page), call.from_user.id))

@dp.callback_query_handler(text_contains='getuser_')
async def getusercall(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    page = call.data.split('_')[2]
    await call.message.delete()
    user_info = db.get_user_info(int(user_id))
    username = user_info[0]
    currency = db.get_currencysetadm()[0]
    courses = get_courses()
    if currency == "rub":
        balance = user_info[1]
    elif currency == "usd":
        balance = (float(user_info[1])/float(courses[0]))
    elif currency == "eur":
        balance = (float(user_info[1])/float(courses[1]))
    pay_count = user_info[2]
    nickame = db.get_usernamerev(int(user_id))
    if pay_count == None:
        pay_count = 0
    userstatus = db.get_userstatus_new(int(user_id))
    mkp = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить баланс'), callback_data=f'changebalance_{user_id}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить статус'), callback_data=f'changestatus_{user_id}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить ник'), callback_data=f'changenockname_{user_id}')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'Выдать промокод'), callback_data=f'givepromo_{user_id}')
    btn5 = types.InlineKeyboardButton(translater(call.from_user.id, 'Обнулить реф'), callback_data=f'obnylrefzar_{user_id}')
    btn6 = types.InlineKeyboardButton(translater(call.from_user.id, 'Установить скидку'), callback_data=f'giveskidka_{user_id}')
    btn7 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отпр. Сообщение'), callback_data=f'sendmsg_{user_id}')
    btn8 = types.InlineKeyboardButton(translater(call.from_user.id, 'Заблокировать'), callback_data=f'ban_{user_id}')
    btn9 = types.InlineKeyboardButton(translater(call.from_user.id, 'Разблокировать'), callback_data=f'banun_{user_id}')
    btn11 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить персональный РЕФ%'), callback_data=f'changepersref_{user_id}')
    btn10 = types.InlineKeyboardButton(translater(call.from_user.id, 'Назад'), callback_data=f'usersback_{page}')
    mkp.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9).add(btn11).add(btn10)
    await call.message.answer(translater(call.from_user.id, 'Статус пользователя:') + f' {userstatus}\n-------------------\n' + translater(call.from_user.id, 'Ник:') + f' {nickame}\n' + translater(call.from_user.id, 'Логин:') + f' @{username}\n' + translater(call.from_user.id, 'Баланс:') + f' {round(float(balance), 2)}\n' + translater(call.from_user.id, 'Персональная скидка:') + f' {db.get_procent(int(user_id))}%\n' + translater(call.from_user.id, 'Персональный РЕФ:') + f' {db.get_refproc_for_user(int(user_id))}%\n' + translater(call.from_user.id, 'Купон на скидку:') + f' {db.get_promoadm(int(user_id)) if db.get_promoadm(int(user_id)) != None else translater(call.from_user.id, "Отсутствует")}\n-------------------\n' + translater(call.from_user.id, 'Личная статистика:\nПокупок:') + f' {pay_count}\n' + translater(call.from_user.id, 'На сумму:') + f' {round(float(db.get_count_buyspr(int(user_id))), 2)}\n' + translater(call.from_user.id, 'Статистика реф.системы:\nРеф. приглашено:') + f' {db.get_count_refs(int(user_id))}\n' + translater(call.from_user.id, 'Реф. заработано:') + f' {round(float(db.get_user_refbalance(int(user_id), currency)), 2)}', reply_markup=mkp)


@dp.callback_query_handler(text_contains='changestatus_')
async def changestatuscall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    userid = call.data.split('_')[1]
    await call.message.answer(translater(call.from_user.id, 'Введите новый статус покупателя:'), reply_markup=cancel_mkp(call.from_user.id))
    await ChangeStatus.UserId.set()
    async with state.proxy() as data:
        data['UserId'] = userid

@dp.message_handler(state=ChangeStatus.UserId)
async def chjangestatususeridmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    user_id = data['UserId']
    db.admchange_status(int(user_id), message.text)
    await message.answer(translater(message.from_user.id, 'Новый статус успешно присвоен!'))
    await state.finish()
    page = 1
    user_info = db.get_user_info(int(user_id))
    username = user_info[0]
    currency = db.get_currencysetadm()[0]
    courses = get_courses()
    if currency == "rub":
        balance = user_info[1]
    elif currency == "usd":
        balance = (float(user_info[1])/float(courses[0]))
    elif currency == "eur":
        balance = (float(user_info[1])/float(courses[1]))
    nickame = db.get_usernamerev(int(user_id))
    pay_count = user_info[2]
    if pay_count == None:
        pay_count = 0
    userstatus = db.get_userstatus_new(int(user_id))
    mkp = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить баланс'), callback_data=f'changebalance_{user_id}')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить статус'), callback_data=f'changestatus_{user_id}')
    btn3 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить ник'), callback_data=f'changenockname_{user_id}')
    btn4 = types.InlineKeyboardButton(translater(message.from_user.id, 'Выдать промокод'), callback_data=f'givepromo_{user_id}')
    btn5 = types.InlineKeyboardButton(translater(message.from_user.id, 'Обнулить реф'), callback_data=f'obnylrefzar_{user_id}')
    btn6 = types.InlineKeyboardButton(translater(message.from_user.id, 'Установить скидку'), callback_data=f'giveskidka_{user_id}')
    btn7 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отпр. Сообщение'), callback_data=f'sendmsg_{user_id}')
    btn8 = types.InlineKeyboardButton(translater(message.from_user.id, 'Заблокировать'), callback_data=f'ban_{user_id}')
    btn9 = types.InlineKeyboardButton(translater(message.from_user.id, 'Разблокировать'), callback_data=f'banun_{user_id}')
    btn11 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить персональный РЕФ%'), callback_data=f'changepersref_{user_id}')
    btn10 = types.InlineKeyboardButton(translater(message.from_user.id, 'Назад'), callback_data=f'usersback_{page}')
    mkp.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9).add(btn11).add(btn10)
    await message.message.answer(translater(message.from_user.id, 'Статус пользователя:') + f' {userstatus}\n-------------------\n' + translater(message.from_user.id, 'Ник:') + f' {nickame}\n' + translater(message.from_user.id, 'Логин:') + f' @{username}\n' + translater(message.from_user.id, 'Баланс:') + f' {round(float(balance), 2)}\n' + translater(message.from_user.id, 'Персональная скидка:') + f' {db.get_procent(int(user_id))}%\n' + translater(message.from_user.id, 'Персональный РЕФ:') + f' {db.get_refproc_for_user(int(user_id))}%\n' + translater(message.from_user.id, 'Купон на скидку:') + f' {db.get_promoadm(int(user_id)) if db.get_promoadm(int(user_id)) != None else translater(message.from_user.id, "Отсутствует")}\n-------------------\n' + translater(message.from_user.id, 'Личная статистика:\nПокупок:') + f' {pay_count}\n' + translater(message.from_user.id, 'На сумму:') + f' {round(float(db.get_count_buyspr(int(user_id))), 2)}\n' + translater(message.from_user.id, 'Статистика реф.системы:\nРеф. приглашено:') + f' {db.get_count_refs(int(user_id))}\n' + translater(message.from_user.id, 'Реф. заработано:') + f' {round(float(db.get_user_refbalance(int(user_id), currency)), 2)}', reply_markup=mkp)
    
@dp.callback_query_handler(text_contains='changestatuss_')
async def changestatusscall(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    procent = call.data.split('_')[2]
    db.updateprocent(int(user_id), int(procent))
    await call.answer('Успешно изменено!', show_alert=True)
    user_info = db.get_user_info(int(user_id))
    username = user_info[0]
    balance = user_info[1]
    nickame = db.get_usernamerev(int(user_id))
    pay_count = user_info[2]
    userstatus = db.get_user_status(int(user_id))
    if userstatus == 'ok':
        userstatus = 'Активный'
    else:
        userstatus = 'Заблокирован'
    mkp = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить баланс'), callback_data=f'changebalance_{user_id}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить статус'), callback_data=f'changestatus_{user_id}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить ник'), callback_data=f'changenockname_{user_id}')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'Выдать промокод'), callback_data=f'givepromo_{user_id}')
    btn5 = types.InlineKeyboardButton(translater(call.from_user.id, 'Обнулить реф'), callback_data=f'obnylrefzar_{user_id}')
    btn6 = types.InlineKeyboardButton(translater(call.from_user.id, 'Установить скидку'), callback_data=f'giveskidka_{user_id}')
    btn7 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отпр. Сообщение'), callback_data=f'sendmsg_{user_id}')
    btn8 = types.InlineKeyboardButton(translater(call.from_user.id, 'Заблокировать'), callback_data=f'ban_{user_id}')
    btn9 = types.InlineKeyboardButton(translater(call.from_user.id, 'Разблокировать'), callback_data=f'banun_{user_id}')
    btn11 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить персональный РЕФ%'), callback_data=f'changepersref_{user_id}')
    btn10 = types.InlineKeyboardButton(translater(call.from_user.id, 'Назад'), callback_data=f'usersback_1')
    mkp.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9).add(btn11).add(btn10)
    await call.message.answer(translater(call.from_user.id, f'Информация о пользователе:') + f'\n-------------------\n' + translater(call.from_user.id, 'Ник:') + f' {nickame}\n' + translater(call.from_user.id, 'Логин:') + f' @{username}\nUserId: {user_id}\n-------------------\n' + translater(call.from_user.id, 'Покупок совершено:') + f' {pay_count}\b' + translater(call.from_user.id, 'Баланс:') + f' {balance}\n' + translater(call.from_user.id, 'Рефералов приглашено:') + f' {db.get_count_refs(int(user_id))}\n' + translater(call.from_user.id, 'Статус пользователя:') + f' {userstatus}', reply_markup=mkp)

@dp.callback_query_handler(text_contains='giveskidka_')
async def giveskidkacall(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[1]
    procent = db.get_procent(int(user_id))
    await call.message.delete()
    await GiveSkidka.UserId.set()
    async with state.proxy() as data:
        data['UserId'] = user_id
    await GiveSkidka.next()
    await call.message.answer(translater(call.from_user.id, 'Скидка пользователя') + f' {procent}%\n' + translater(call.from_user.id, 'Введите новую скидку:'), reply_markup=cancel_mkp(call.from_user.id))

@dp.message_handler(state=GiveSkidka.Skidka)
async def giveskidkaskidkamsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            pass
        user_id = data['UserId']
        db.updateprocent(int(user_id), int(message.text))
        await message.answer(translater(message.from_user.id, 'Скидка успешно обновлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
        await state.finish()
    else:
        await message.answer(translater(message.from_user.id, 'Введите процент скидки целым числом'), reply_markup=cancel_mkp(message.from_user.id))

@dp.callback_query_handler(text_contains='sendmsg_')
async def sendmsgcall(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[1]
    await call.message.delete()
    await SendMsg.UserId.set()
    async with state.proxy() as data:
        data['UserId'] = user_id
    await call.message.answer(translater(call.from_user.id, 'Введите сообщение. Его получит пользователь с ID') + f' <code>{user_id}</code>', reply_markup=cancel_mkp(call.from_user.id))

@dp.message_handler(content_types=['text', 'photo', 'video'], state=SendMsg.UserId)
async def sendmsguseridmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    user_id = data['UserId']
    try:
        await bot.copy_message(int(user_id), message.from_user.id, message.message_id)       
    except:
        pass
    await message.answer(translater(message.from_user.id, 'Сообщение отправлено. Введите ещё или нажмите "Отменить"'), reply_markup=cancel_mkp(message.from_user.id))

@dp.callback_query_handler(text_contains='givepromo_')
async def givepromocall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await GivePromo.UserId.set()
    async with state.proxy() as data:
        data['UserId'] = call.data.split('_')[1]
    await GivePromo.next()
    await call.message.answer(translater(call.from_user.id, 'Введите промокод:'), reply_markup=cancel_mkp(call.from_user.id))

@dp.message_handler(state=GivePromo.Promo)
async def givepromopromomsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Promo'] = message.text
    await GivePromo.next()
    await message.answer(translater(message.from_user.id, 'Хорошо, введите процент скидки (целым числом)'), reply_markup=cancel_mkp(message.from_user.id))

@dp.message_handler(state=GivePromo.Procent)
async def givepromoprocentmsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['Procent'] = message.text
        userid = data['UserId']
        promo = data['Promo']
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Да'), callback_data='go')
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
        mkp.add(btn1).add(btn2)
        await message.answer(translater(message.from_user.id, 'Вы действительно хотите выдать пользователю с ID') + f' <code>{userid}</code>\n' + translater(message.from_user.id, 'Промокод:') + f' <code>{promo}</code>\n' + translater(message.from_user.id, 'Со скидкой в') + f' {message.text}%', reply_markup=mkp)
    else:
        await message.answer(translater(message.from_user.id, 'Введите процент скидки целым числом'), reply_markup=cancel_mkp(message.from_user.id))


@dp.callback_query_handler(text='go', state=GivePromo.Procent)
async def givepromoprocentgocall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        pass
    userid = data['UserId']
    promo = data['Promo']
    procent = data['Procent']
    db.add_promo(promo, int(userid), procent)
    try:
        await bot.send_message(int(userid), translater(call.from_user.id, f'Вам был выдан промокод на') + f' {procent}% ' + translater(call.from_user.id, f'скидку!\nПромокод:') + f' <code>{promo}</code>')
    except:
        pass
    await call.message.answer(translater(call.from_user.id, 'Пользователю успешно выдан промокод! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='changebalance_')
async def changebalancecall(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[1]
    balance = db.get_balance(int(user_id))
    await call.message.delete()
    await ChangeBalance.UserId.set()
    async with state.proxy() as data:
        data['UserId'] = user_id
    await ChangeBalance.next()
    await call.message.answer(translater(call.from_user.id, 'Баланс пользователя:') + f' {balance}\n' + translater(call.from_user.id, 'Введите новый баланс (в рублях):'), reply_markup=cancel_mkp(call.from_user.id))

@dp.callback_query_handler(text='cancel', state=ChangeBalance.Balance)
@dp.callback_query_handler(text='cancel', state=ChangeRef.Ref)
@dp.callback_query_handler(text='cancel', state=GivePromo.Procent)
@dp.callback_query_handler(text='cancel', state=GivePromo.Promo)
@dp.callback_query_handler(text='cancel', state=GiveSkidka.Skidka)
@dp.callback_query_handler(text='cancel', state=SendMsg.UserId)
async def cancelchangebalance(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=ChangeBalance.Balance)
async def changebalancebalancemsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            pass
        userid = data['UserId']
        db.change_balance(int(userid), message.text)
        await message.answer(translater(message.from_user.id, 'Баланс успешно изменен! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
        await state.finish()
    else:
        message.answer(translater(message.from_user.id, 'Введите новый баланс целым числом!'), reply_markup=cancel_mkp(message.from_user.id))



@dp.callback_query_handler(text_contains='changepersref_')
async def changepersproccall(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[1]
    procent = db.get_refproc_for_user(int(user_id))
    await call.message.delete()
    await ChangeRef2.UserId.set()
    async with state.proxy() as data:
        data['UserId'] = user_id
    await ChangeRef2.next()
    await call.message.answer(translater(call.from_user.id, 'Персональный реф. процент юзера:') + f' {procent}\n' + translater(call.from_user.id, 'Введите новый процент:'), reply_markup=cancel_mkp(call.from_user.id))

@dp.message_handler(state=ChangeRef2.Ref)
async def changepersprocmsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            pass
        userid = data['UserId']
        # await message.answer(f'{userid} | {int(message.text)}')
        db.update_personal_procent(int(userid), int(message.text))
        await message.answer(translater(message.from_user.id, 'Персональный реф. процент изменен! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
        await state.finish()
    else:
        message.answer(translater(message.from_user.id, 'Введите персональный реф. процент целым числом!'), reply_markup=cancel_mkp(message.from_user.id))



@dp.callback_query_handler(text_contains='ban_')
async def bancall(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    db.ban_user(int(user_id))
    await call.message.answer(translater(call.from_user.id, 'Пользователь заблокирован. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    try:
        await bot.send_message(int(user_id), translater(call.from_user.id, 'Вы были заблокированы'))
    except:
        pass

@dp.callback_query_handler(text_contains='banun_')
async def banuncall(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    db.unban_user(int(user_id))
    await call.message.answer(translater(call.from_user.id, 'Пользователь разблокирован. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    try:
        await bot.send_message(int(user_id), translater(call.from_user.id, 'Вы были разблокированы. Пропишите /start для обновления'))
    except:
        pass

@dp.message_handler(text='Настройка доставки')
@dp.message_handler(text='Delivery settings')
async def deliverysetadminmsg(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(translater(message.from_user.id, 'Варианты доставки'), reply_markup=deliveriesadm_mkp(message.from_user.id))

@dp.callback_query_handler(text='deliveryadd')
async def deliveryaddcall(call: types.CallbackQuery):
    await call.message.delete()
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название доставки:'), reply_markup=cancel_mkp(call.from_user.id))
    elif check_lan[0] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название доставки:'), reply_markup=cancel_mkp(call.from_user.id))
    elif check_lan[1] == 1:
        await call.message.answer(translater(call.from_user.id, 'Введите название доставки на английском:'), reply_markup=cancel_mkp(call.from_user.id))
    await DeliveryAdd.Name.set()

@dp.callback_query_handler(text='cancel', state=DeliveryAdd.Name)
@dp.callback_query_handler(text='cancel', state=DeliveryAdd.EngName)
@dp.callback_query_handler(text='cancel', state=DeliveryAdd.Cost)
async def canceldeliveryaddcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=DeliveryAdd.Name)
async def deliveryaddnamemsg(message: types.Message, state: FSMContext):
    check_lan = db.check_lanadd()
    if check_lan[0] == 1 and check_lan[1] == 1:
        async with state.proxy() as data:
            data['Name'] = message.text
        await message.answer(translater(message.from_user.id, 'Введите название на английском:'), reply_markup=cancel_mkp(message.from_user.id))
    elif check_lan[0] == 1:
        async with state.proxy() as data:
            data['Name'] = message.text
        await DeliveryAdd.next()
        async with state.proxy() as data:
            data['EngName'] = 'None'
        await message.answer(translater(message.from_user.id, 'Введите стоимость доставки:'), reply_markup=cancel_mkp(message.from_user.id))
    elif check_lan[1] == 1:
        async with state.proxy() as data:
            data['Name'] = 'None'
        await DeliveryAdd.next()
        async with state.proxy() as data:
            data['EngName'] = message.text
        await message.answer(translater(message.from_user.id, 'Введите стоимость доставки:'), reply_markup=cancel_mkp(message.from_user.id))
    await DeliveryAdd.next()

@dp.message_handler(state=DeliveryAdd.EngName)
async def deliveryaddengnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['EngName'] = message.text
    await message.answer(translater(message.from_user.id, 'Введите стоимость доставки:'), reply_markup=cancel_mkp(message.from_user.id))
    await DeliveryAdd.next()

@dp.message_handler(state=DeliveryAdd.Cost)
async def deliveryaddcostmsg(message: types.Message, state: FSMContext):
    try:
        cost = float(message.text)
        async with state.proxy() as data:
            data['Cost'] = cost
        name = data['Name']
        engname = data['EngName']
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Да'), callback_data='go')
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
        mkp.add(btn1).add(btn2)
        await message.answer(translater(message.from_user.id, 'Вы действительно хотите добавить вариант доставки:\n<b>Название</b>:') + f' <code>{name}</code>\n<b>' + translater(message.from_user.id, 'На английском:') + f'</b> <code>{engname}</code>\n<b>' + translater(message.from_user.id, 'Стоимость') + f'</b>: <code>{cost}</code>', reply_markup=mkp)
    except:
        await message.answer(translater(message.from_user.id, 'Введите стоимость доставки целым числом или через точку. Пример: <code>143.55</code>'), reply_markup=cancel_mkp(message.from_user.id))

@dp.callback_query_handler(text='go', state=DeliveryAdd.Cost)
async def deliveryaddgocall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    name = data['Name']
    engname = data['EngName']
    cost = data['Cost']
    currency = db.get_currencysetadm()[0]
    db.add_delivery_adm(name, engname, cost, currency)
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Доставка успешно добавлена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.callback_query_handler(text_contains='admdeliveryset_')
async def admdeliverysetcall(call: types.CallbackQuery):
    deliveryid = call.data.split('_')[1]
    delinfo = db.get_delivery_info(int(deliveryid))
    await call.message.delete()
    if delinfo[2] == 'off':
        status = 'Выключена'
        btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Включить'), callback_data=f'deliveryon_{deliveryid}')
    elif delinfo[2] == 'on':
        status = 'Включена'
        btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Выключить'), callback_data=f'deliveryoff_{deliveryid}')
    mkp = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить название'), callback_data=f'deliverychangename_{deliveryid}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить стоимость'), callback_data=f'deliverychangecost_{deliveryid}')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить доставку'), callback_data=f'deliverydelete_{deliveryid}')
    btn5 = types.InlineKeyboardButton(translater(call.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5)
    await call.message.answer(translater(call.from_user.id, 'Название:') + f' {delinfo[0]}\n' + translater(call.from_user.id, 'Стоимость:') + f' {delinfo[1]}\n' + translater(call.from_user.id, 'Статус:') + f' ' + translater(call.from_user.id, f'{status}'),  reply_markup=mkp)

@dp.callback_query_handler(text_contains='deliveryon_')
async def deliveryoncall(call: types.CallbackQuery):
    deliveryid = call.data.split('_')[1]
    db.delivery_stat(int(deliveryid), 'on')
    delinfo = db.get_delivery_info(int(deliveryid))
    await call.message.delete()
    if delinfo[2] == 'off':
        status = 'Выключена'
        btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Включить'), callback_data=f'deliveryon_{deliveryid}')
    elif delinfo[2] == 'on':
        status = 'Включена'
        btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Выключить'), callback_data=f'deliveryoff_{deliveryid}')
    mkp = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить название'), callback_data=f'deliverychangename_{deliveryid}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить стоимость'), callback_data=f'deliverychangecost_{deliveryid}')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить доставку'), callback_data=f'deliverydelete_{deliveryid}')
    btn5 = types.InlineKeyboardButton(translater(call.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5)
    await call.message.answer(translater(call.from_user.id, 'Название:') + f' {delinfo[0]}\n' + translater(call.from_user.id, 'Стоимость:') + f' {delinfo[1]}\n' + translater(call.from_user.id, 'Статус:') + f' ' + translater(call.from_user.id, f'{status}'), reply_markup=mkp)

@dp.callback_query_handler(text_contains='deliveryoff_')
async def deliveryoffcall(call: types.CallbackQuery):
    deliveryid = call.data.split('_')[1]
    db.delivery_stat(int(deliveryid), 'off')
    delinfo = db.get_delivery_info(int(deliveryid))
    await call.message.delete()
    if delinfo[2] == 'off':
        status = 'Выключена'
        btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Включить'), callback_data=f'deliveryon_{deliveryid}')
    elif delinfo[2] == 'on':
        status = 'Включена'
        btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Выключить'), callback_data=f'deliveryoff_{deliveryid}')
    mkp = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить название'), callback_data=f'deliverychangename_{deliveryid}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Изменить стоимость'), callback_data=f'deliverychangecost_{deliveryid}')
    btn4 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить доставку'), callback_data=f'deliverydelete_{deliveryid}')
    btn5 = types.InlineKeyboardButton(translater(call.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5)
    await call.message.answer(translater(call.from_user.id, 'Название:') + f' {delinfo[0]}\n' + translater(call.from_user.id, 'Стоимость:') + f' {delinfo[1]}\n' + translater(call.from_user.id, 'Статус:') + f' ' + translater(call.from_user.id, f'{status}'), reply_markup=mkp)

@dp.callback_query_handler(text_contains='deliverychangename_')
async def deliverychnamecall(call: types.CallbackQuery, state: FSMContext):
    deliveryid = call.data.split('_')[1]
    delinfo = db.get_delivery_info(int(deliveryid))
    await DeliveryChangeName.DeliveryId.set()
    async with state.proxy() as data:
        data['DeliveryId'] = deliveryid
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Название доставки:') + f' <code>{delinfo[0]}</code>\n' + translater(call.from_user.id, 'Введите новое название'), reply_markup=cancel_mkp(call.from_user.id))
    await DeliveryChangeName.next()

@dp.callback_query_handler(text='cancel', state=DeliveryChangeName.Name)
@dp.callback_query_handler(text='cancel', state=DeliveryChangeName.EngName)
@dp.callback_query_handler(text='cancel', state=DeliveryChangeCost.Cost)
async def canceldelchnamecall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=DeliveryChangeName.Name)
async def delchnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    await message.answer(translater(message.from_user.id, 'Введите название доставки на английском:'), reply_markup=cancel_mkp(message.from_user.id))
    await DeliveryChangeName.next()

@dp.message_handler(state=DeliveryChangeName.EngName)
async def deliverychangenameengname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    name = data['Name']
    engname = message.text
    deliveryid = data['DeliveryId']
    db.change_delivery_name(int(deliveryid), name, engname)
    await message.answer(translater(message.from_user.id, 'Успешно изменено!'))
    await state.finish()
    delinfo = db.get_delivery_info(int(deliveryid))
    if delinfo[2] == 'off':
        status = 'Выключена'
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Включить'), callback_data=f'deliveryon_{deliveryid}')
    elif delinfo[2] == 'on':
        status = 'Включена'
        btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Выключить'), callback_data=f'deliveryoff_{deliveryid}')
    mkp = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить название'), callback_data=f'deliverychangename_{deliveryid}')
    btn3 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить стоимость'), callback_data=f'deliverychangecost_{deliveryid}')
    btn4 = types.InlineKeyboardButton(translater(message.from_user.id, 'Удалить доставку'), callback_data=f'deliverydelete_{deliveryid}')
    btn5 = types.InlineKeyboardButton(translater(message.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5)
    await message.answer(translater(message.from_user.id, 'Название:') + f' {delinfo[0]}\n' + translater(message.from_user.id, 'Стоимость:') + f' {delinfo[1]}\n' + translater(message.from_user.id, 'Статус:') + f' ' + translater(message.from_user.id, f'{status}'), reply_markup=mkp)

@dp.callback_query_handler(text_contains='deliverychangecost_')
async def deliverychangecostcall(call: types.CallbackQuery, state: FSMContext):
    deliveryid = call.data.split('_')[1]
    delinfo = db.get_delivery_info(int(deliveryid))
    await DeliveryChangeCost.DeliveryId.set()
    async with state.proxy() as data:
        data['DeliveryId'] = deliveryid
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Старая цена доставки:') + f' {delinfo[1]}\n' + translater(call.from_user.id, 'Введите новую'), reply_markup=cancel_mkp(call.from_user.id))
    await DeliveryChangeCost.next()

@dp.message_handler(state=DeliveryChangeCost.Cost)
async def delchcostmsg(message: types.Message, state: FSMContext):
    try:
        cost = float(message.text)
        async with state.proxy() as data:
            pass
        deliveryid = data['DeliveryId']
        db.change_delivery_cost(int(deliveryid), str(cost))
        await message.answer(translater(message.from_user.id, 'Цена успешно изменена!'))
        await state.finish()
        delinfo = db.get_delivery_info(int(deliveryid))
        if delinfo[2] == 'off':
            status = 'Выключена'
            btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Включить'), callback_data=f'deliveryon_{deliveryid}')
        elif delinfo[2] == 'on':
            status = 'Включена'
            btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Выключить'), callback_data=f'deliveryoff_{deliveryid}')
        mkp = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить название'), callback_data=f'deliverychangename_{deliveryid}')
        btn3 = types.InlineKeyboardButton(translater(message.from_user.id, 'Изменить стоимость'), callback_data=f'deliverychangecost_{deliveryid}')
        btn4 = types.InlineKeyboardButton(translater(message.from_user.id, 'Удалить доставку'), callback_data=f'deliverydelete_{deliveryid}')
        btn5 = types.InlineKeyboardButton(translater(message.from_user.id, 'Админ-панель'), callback_data='admin')
        mkp.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5)
        await message.answer(translater(message.from_user.id, 'Название:') + f' {delinfo[0]}\n' + translater(message.from_user.id, 'Стоимость:') + f' {delinfo[1]}\n' + translater(message.from_user.id, 'Статус:') + f' ' + translater(message.from_user.id, f'{status}'), reply_markup=mkp)
    except:
        await message.answer(translater(message.from_user.id, 'Введите новую цену целым числом или через точку. Пример: <code>145.31</code>'), reply_markup=cancel_mkp(message.from_user.id))

@dp.callback_query_handler(text_contains='deliverydelete_')
async def deliverydeletecall(call: types.CallbackQuery):
    deliveryid = call.data.split('_')[1]
    await call.message.delete()
    delinfo = db.get_delivery_info(int(deliveryid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Удалить'), callback_data=f'deliverydeletee_{deliveryid}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data=f'admdeliveryset_{deliveryid}')
    mkp.add(btn1).add(btn2)
    await call.message.answer(translater(call.from_user.id, 'Вы действительно хотите удалить способ доставки') + f' "{delinfo[0]}"', reply_markup=mkp)

@dp.callback_query_handler(text_contains='deliverydeletee_')
async def deliverydeleteecall(call: types.CallbackQuery):
    deliveryid = call.data.split('_')[1]
    db.del_delivery(int(deliveryid))
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Доставка успешно удалена! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))


@dp.message_handler(text='Платежные системы')
@dp.message_handler(text='Payment systems')
async def platezhsistemmsg(message: types.Message):
    qiwistat = db.get_qiwi_stat()
    cryptostat = db.get_crypto_stat()
    yoomoneystat = db.get_yoomoney_stat()
    mkp = types.InlineKeyboardMarkup()
    if qiwistat == 'on':
        btn1 = types.InlineKeyboardButton('✅ QIWI', callback_data='changepaym_qiwi')
    else:
        btn1 = types.InlineKeyboardButton('❌ QIWI', callback_data='changepaym_qiwi')
    
    if cryptostat == 'on':
        btn2 = types.InlineKeyboardButton('✅ CRYPTO', callback_data='changepaym_crypto')
    else:
        btn2 = types.InlineKeyboardButton('❌ CRYPTO', callback_data='changepaym_crypto')
    if yoomoneystat == 'on':
        btn3 = types.InlineKeyboardButton('✅ YOOMONEY', callback_data='changepaym_yoomoney')
    else:
        btn3 = types.InlineKeyboardButton('❌ YOOMONEY', callback_data='changepaym_yoomoney')
    btn4 = types.InlineKeyboardButton(translater(message.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp.add(types.InlineKeyboardButton('QIWI', callback_data='getpaym_qiwi')).add(types.InlineKeyboardButton('CRYPTO', callback_data='getpaym_crypto')).add(types.InlineKeyboardButton('YOOMONEY', callback_data='getpaym_yoomoney')).add(btn4)
    # mkp.add(btn1).add(types.InlineKeyboardButton('Токен Qiwi', callback_data='changetoken_QIWI')).add(btn2).add(types.InlineKeyboardButton('Токен Crypto', callback_data='changetoken_CRYPTO')).add(btn3).add(types.InlineKeyboardButton('Токен Yoomoney', callback_data='changetoken_YOOMONEY')).add(btn4)
    await message.answer(translater(message.from_user.id, 'Платежные системы:'), reply_markup=mkp)

@dp.callback_query_handler(text_contains='getpaym_')
async def getpaymcall(call: types.CallbackQuery):
    paym = call.data.split('_')[1]
    qiwistat = db.get_qiwi_stat()
    cryptostat = db.get_crypto_stat()
    yoomoneystat = db.get_yoomoney_stat()
    
    
    
    
    
    if paym == 'qiwi':
        if qiwistat == 'on':
            btn1 = types.InlineKeyboardButton('✅ QIWI', callback_data='changepaym_qiwi')
        else:
            btn1 = types.InlineKeyboardButton('❌ QIWI', callback_data='changepaym_qiwi')
        btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Токен') + ' Qiwi', callback_data='changetoken_QIWI')
    elif paym == 'crypto':
        if cryptostat == 'on':
            btn1 = types.InlineKeyboardButton('✅ CRYPTO', callback_data='changepaym_crypto')
        else:
            btn1 = types.InlineKeyboardButton('❌ CRYPTO', callback_data='changepaym_crypto')
        btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Токен') + ' Crypto', callback_data='changetoken_CRYPTO')
    elif paym == 'yoomoney':
        if yoomoneystat == 'on':
            btn1 = types.InlineKeyboardButton('✅ YOOMONEY', callback_data='changepaym_yoomoney')
        else:
            btn1 = types.InlineKeyboardButton('❌ YOOMONEY', callback_data='changepaym_yoomoney')
        btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Токен') + ' Yoomoney', callback_data='changetoken_YOOMONEY')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp = types.InlineKeyboardMarkup()
    mkp.add(btn1).add(btn2).add(btn3)
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Выберите действие:'), reply_markup=mkp)



@dp.callback_query_handler(text_contains='changepaym_')
async def changepaymcall(call: types.CallbackQuery):
    paym = call.data.split('_')[1]
    if paym == 'qiwi':
        paym = 'QIWI'
    elif paym == 'crypto':
        paym = 'CRYPTO'
    elif paym == 'yoomoney':
        paym = 'YOOMONEY'
    db.change_paym(paym)
    qiwistat = db.get_qiwi_stat()
    cryptostat = db.get_crypto_stat()
    yoomoneystat = db.get_yoomoney_stat()
    if paym == 'QIWI':
        if qiwistat == 'on':
            btn1 = types.InlineKeyboardButton('✅ QIWI', callback_data='changepaym_qiwi')
        else:
            btn1 = types.InlineKeyboardButton('❌ QIWI', callback_data='changepaym_qiwi')
        btn2 = types.InlineKeyboardButton('Токен Qiwi', callback_data='changetoken_QIWI')
    elif paym == 'CRYPTO':
        if cryptostat == 'on':
            btn1 = types.InlineKeyboardButton('✅ CRYPTO', callback_data='changepaym_crypto')
        else:
            btn1 = types.InlineKeyboardButton('❌ CRYPTO', callback_data='changepaym_crypto')
        btn2 = types.InlineKeyboardButton('Токен Crypto', callback_data='changetoken_CRYPTO')
    elif paym == 'YOOMONEY':
        if yoomoneystat == 'on':
            btn1 = types.InlineKeyboardButton('✅ YOOMONEY', callback_data='changepaym_yoomoney')
        else:
            btn1 = types.InlineKeyboardButton('❌ YOOMONEY', callback_data='changepaym_yoomoney')
        btn2 = types.InlineKeyboardButton('Токен Yoomoney', callback_data='changetoken_YOOMONEY')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp = types.InlineKeyboardMarkup().add(btn1).add(btn2).add(btn3)
    await call.message.edit_reply_markup(mkp)


@dp.callback_query_handler(text_contains='changetoken_')
async def changetokencall(call: types.CallbackQuery, state: FSMContext):
    paym = call.data.split('_')[1]
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Введите новый токен для') + f' {paym}:', reply_markup=cancel_mkp(call.from_user.id))
    await ChangeToken.Paym.set()
    async with state.proxy() as data:
        data['Paym'] = paym
    await ChangeToken.next()

@dp.message_handler(state=ChangeToken.Token)
async def changetokentokenmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Token'] = message.text
    paym = data['Paym']
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Да'), callback_data='go')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer(translater(message.from_user.id, 'Вы действительно хотите изменить токен') + f' {paym} ' + translater(message.from_user.id, 'на') + f' <code>{message.text}</code>', reply_markup=mkp)

@dp.callback_query_handler(text='cancel', state=ChangeToken.Token)
async def changetokencancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.callback_query_handler(text='go', state=ChangeToken.Token)
async def changetokengocall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        pass
    paym = data['Paym']
    token = data['Token']
    db.changetoken(paym, token)
    await call.message.answer(translater(call.from_user.id, 'Токен успешно изменен. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()


@dp.message_handler(text='Заявки на вывод')
@dp.message_handler(text='Requests for withdrawal')
async def withdrawsadm(message: types.Message, state: FSMContext):
    if message.from_user.id in admins:
        await message.answer(translater(message.from_user.id, 'Список заявок на вывод:'), reply_markup=withdraws_mkp(message.from_user.id))

@dp.callback_query_handler(text_contains='withdr_')
async def withdrcall(call: types.CallbackQuery):
    with_id = call.data.split('_')[1]
    await call.message.delete()
    with_info = db.get_withdraw(int(with_id))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Выплачено'), callback_data=f'withok_{with_id}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отказано'), callback_data=f'withno_{with_id}')
    btn3 = types.InlineKeyboardButton(translater(call.from_user.id, 'Админ-панель'), callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3)
    await call.message.answer(translater(call.from_user.id, 'ID пользователя:') + f' {with_info[0]}\n' + translater(call.from_user.id, 'Сумма:') + f' {with_info[1]}\n' + translater(call.from_user.id, 'Реквизиты:') + f' {with_info[2]}', reply_markup=mkp)


@dp.callback_query_handler(text_contains='withok_')
async def withokcall(call: types.CallbackQuery):
    with_id = call.data.split('_')[1]
    with_info = db.get_withdraw(int(with_id))
    db.with_del(int(with_id))
    try:
        await bot.send_message(int(with_info[0]), translater(call.from_user.id, 'Ваша заявка на выплату успешно выплачена!'))
    except:
        pass
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Пользователь получил уведомление! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))


@dp.callback_query_handler(text_contains='withno_')
async def withokcall(call: types.CallbackQuery):
    with_id = call.data.split('_')[1]
    with_info = db.get_withdraw(int(with_id))
    db.with_del(with_id)
    db.add_balance(int(with_info[0]), float(with_info[1]))
    try:
        await bot.send_message(int(with_info[0]), translater(call.from_user.id, 'Ваша заявка на выплату отклонена!'))
    except:
        pass
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Пользователь получил уведомление! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))


@dp.message_handler(text='Настройки бота')
@dp.message_handler(text='Bot settings')
async def botsettingsmsg(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(translater(message.from_user.id, 'Вы перешли в настройки бота'), reply_markup=botsettings_mkp(message.from_user.id))

@dp.message_handler(text='Изменить правила')
@dp.message_handler(text='Change rules')
async def changerulesmsg(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(translater(message.from_user.id, 'Текущие правила:'))
        await message.answer(db.get_rules())
        await message.answer(translater(message.from_user.id, 'Введите новый правила:'), reply_markup=cancel_mkp(message.from_user.id))
        await ChangeRules.Rules.set()


@dp.callback_query_handler(text='cancel', state=ChangeRules.Rules)
async def cancelchangerulescall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=ChangeRules.Rules)
async def changerulesrulesmsg(message: types.Message, state: FSMContext):
    db.changerules(message.text)
    await message.answer(translater(message.from_user.id, 'Правила успешно обновлены! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()

@dp.message_handler(text='Изменить токен бота')
@dp.message_handler(text='Change bot token')
async def changetokebotadm(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(translater(message.from_user.id, 'Введите новый токен бота. Внимание, если вы введете некорректный токен - бот сломается'), reply_markup=cancel_mkp(message.from_user.id))
        await ChangeToken.Token.set()

@dp.callback_query_handler(text='cancel', state=ChangeToken.Token)
async def cancelchangetokencall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=ChangeToken.Token)
async def changetokentokenmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Token'] = message.text
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(message.from_user.id, 'Да'), callback_data='go')
    btn2 = types.InlineKeyboardButton(translater(message.from_user.id, 'Отменить'), callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer(translater(message.from_user.id, 'Вы действительно хотите изменить токен бота на') + f' <code>{message.text}</code>', reply_markup=mkp)

@dp.callback_query_handler(text='go', state=ChangeToken.Token)
async def changetokengocall(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Изменяю токен...', show_alert=True)
    await call.message.delete()
    async with state.proxy() as data:
        pass
    token = data['Token']
    db.change_bottoken(token)
    await call.message.answer(translater(call.from_user.id, 'Токен изменен! Перезапустите бота для применения изменений'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(text='Плата за отзыв')
@dp.message_handler(text='Review fee')
async def platazaotzivpy(message: types.Message):
    reviewpay = db.get_reviewpay()
    await message.answer(translater(message.from_user.id, 'Сейчас мы платим') + f' {reviewpay} ' + translater(message.from_user.id, 'руб за отзыв. Введите новое число или нажмите "Отменить"'), reply_markup=cancel_mkp(message.from_user.id))
    await ChangeReviewPay.Pay.set()

@dp.callback_query_handler(text='cancel', state=ChangeReviewPay.Pay)
async def changereviewpaycancelcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=ChangeReviewPay.Pay)
async def changereviewpaypaymsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['Pay'] = message.text
        db.change_reviewpay(message.text)
        await message.answer(translater(message.from_user.id, 'Успешно изменено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
        await state.finish()
    else:
        await message.answer(translater(message.from_user.id, 'Введите сумму, которую будем платить пользователю за отзыв целым числом:'), reply_markup=cancel_mkp(message.from_user.id))

@dp.message_handler(text='Настройка языка')
@dp.message_handler(text='Language setting')
async def lansetadm(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(translater(message.from_user.id, 'Настройки языка:'), reply_markup=lan_settingmkp(message.from_user.id))

@dp.callback_query_handler(text_contains='setlanset_')
async def setlansetcall(call: types.CallbackQuery):
    lan = call.data.split('_')[1]
    if lan == 'ru':
        db.changestatlan_ru()
    elif lan == 'en':
        db.changestatlan_en()
    await call.message.edit_reply_markup(lan_settingmkp(call.from_user.id))


@dp.callback_query_handler(text_contains='changenockname_')
async def changenocknamecall(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[1]
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Введите новый никнейм:'), reply_markup=cancel_mkp(call.from_user.id))
    await ChageNicknameAdm.UserId.set()
    async with state.proxy() as data:
        data['UserId'] = user_id
    await ChageNicknameAdm.next()

@dp.callback_query_handler(text='cancel', state=ChageNicknameAdm.Nickname)
async def cancelchangenicknameadm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(translater(call.from_user.id, 'Отменено. Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))
    await state.finish()

@dp.message_handler(state=ChageNicknameAdm.Nickname)
async def changenicknameadmmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    user_id = data['UserId']
    db.update_usernamerev(message.text, int(user_id))
    await message.answer(translater(message.from_user.id, 'Никнейм успешно изменен! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(message.from_user.id))
    await state.finish()



@dp.callback_query_handler(text_contains='obnylrefzar_')
async def oblylrefzarcall(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(translater(call.from_user.id, 'Да'), callback_data=f'obnylrefzarr_{user_id}')
    btn2 = types.InlineKeyboardButton(translater(call.from_user.id, 'Отменить'), callback_data='admin')
    mkp.add(btn1).add(btn2)
    await call.message.answer(translater(call.from_user.id, 'Вы действительно хотите обнулить заработок реф?'), reply_markup=mkp)

@dp.callback_query_handler(text_contains='obnylrefzarr_')
async def obnylrefzarrcall(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    await call.message.delete()
    db.obnyl_refbal(int(user_id))
    await call.message.answer(translater(call.from_user.id, 'Успешно обнулено! Вы были возвращены в админ-панель'), reply_markup=admin_mkp(call.from_user.id))

@dp.message_handler(commands='resetprice')
async def resetpricecmd(message: types.Message):
    if message.from_user.id in admins:
        db.update_pricesgood()
        await message.answer(translater(message.from_user.id, 'Цены обновлены'))


@dp.message_handler(text='Настройка валют')
@dp.message_handler(text='Currency settings')
async def setvalut(message: types.Message):
    if message.from_user.id in admins:
        currencyinfo = db.get_currencysetadm()[0]
        mkp = types.InlineKeyboardMarkup()
        if currencyinfo == 'rub':
            btn1 = types.InlineKeyboardButton('✅ RUB', callback_data='none')
        else:
            btn1 = types.InlineKeyboardButton('❌ RUB', callback_data='currencyon_rub')
        if currencyinfo == 'usd':
            btn2 = types.InlineKeyboardButton('✅ USD', callback_data='none')
        else:
            btn2 = types.InlineKeyboardButton('❌ USD', callback_data='currencyon_usd')
        if currencyinfo == 'eur':
            btn3 = types.InlineKeyboardButton('✅ EUR', callback_data='none')
        else:
            btn3 = types.InlineKeyboardButton('❌ EUR', callback_data='currencyon_eur')
        mkp.add(btn1).add(btn2).add(btn3).add(types.InlineKeyboardButton(translater(message.from_user.id, 'Админ-панель'), callback_data='admin'))
        await message.answer(translater(message.from_user.id, 'Настройки валют:'), reply_markup=mkp)
        
@dp.callback_query_handler(text_contains='currencyon_')
async def currencyoncall(call: types.CallbackQuery):
    currency = call.data.split('_')[1]
    db.upd_currencyon(currency)
    currencyinfo = db.get_currencysetadm()[0]
    mkp = types.InlineKeyboardMarkup()
    if currencyinfo == 'rub':
        btn1 = types.InlineKeyboardButton('✅ RUB', callback_data='none')
    else:
        btn1 = types.InlineKeyboardButton('❌ RUB', callback_data='currencyon_rub')
    if currencyinfo == 'usd':
        btn2 = types.InlineKeyboardButton('✅ USD', callback_data='none')
    else:
        btn2 = types.InlineKeyboardButton('❌ USD', callback_data='currencyon_usd')
    if currencyinfo == 'eur':
        btn3 = types.InlineKeyboardButton('✅ EUR', callback_data='none')
    else:
        btn3 = types.InlineKeyboardButton('❌ EUR', callback_data='currencyon_eur')
    mkp.add(btn1).add(btn2).add(btn3).add(types.InlineKeyboardButton(translater(call.from_user.id, 'Админ-панель'), callback_data='admin'))
    await call.message.edit_reply_markup(mkp)
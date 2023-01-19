from aiogram.dispatcher.filters.state import State, StatesGroup


class SuppUser(StatesGroup):
    UserId = State()

class SuppAdmin(StatesGroup):
    UserId = State()
    QuestId = State()
    Text = State()

class AddSupport(StatesGroup):
    UserId = State()

class NewFaq(StatesGroup):
    Name = State()
    EngName = State()
    Text = State()
    EngText = State()
    Photo = State()

class FaqName(StatesGroup):
    FaqId = State()
    Name = State()

class FaqText(StatesGroup):
    FaqId = State()
    Text = State()
    
class AddCat(StatesGroup):
    CatName = State()
    EngCatName = State()

class AddCatRus(StatesGroup):
    CatName = State()

class AddCatEng(StatesGroup):
    CatName = State()

class ChangeNamecat(StatesGroup):
    CatId = State()
    CatName = State()

class ChangeNamecatRus(StatesGroup):
    CatId = State()
    CatName = State()

class ChangeNamecatEng(StatesGroup):
    CatId = State()
    CatName = State()

class AddSubcat(StatesGroup):
    CatId = State()
    SubcatName = State()
    SubcatEngName = State()

class AddSubcatRus(StatesGroup):
    CatId = State()
    SubcatName = State()

class AddSubcatEng(StatesGroup):
    CatId = State()
    SubcatName = State()

class ChangeNamesubcat(StatesGroup):
    SubcatId = State()
    SubcatName = State()

class ChangeNamesubcatRus(StatesGroup):
    SubcatId = State()
    SubcatName = State()

class ChangeNamesubcatEng(StatesGroup):
    SubcatId = State()
    SubcatName = State()

class AddGood(StatesGroup):
    SubcatId = State()
    CatId = State()
    Name = State()
    EngName = State()
    Description = State()
    EngDescription = State()
    Photo = State()
    Price = State()

class ChangeNameGood(StatesGroup):
    GoodId = State()
    GoodName = State()

class ChangeNameGoodRus(StatesGroup):
    GoodId = State()
    GoodName = State()

class ChangeNameGoodEng(StatesGroup):
    GoodId = State()
    GoodName = State()

class ChangeDescGood(StatesGroup):
    GoodId = State()
    GoodDesc = State()

class ChangeDescGoodRus(StatesGroup):
    GoodId = State()
    GoodDesc = State()

class ChangeDescGoodEng(StatesGroup):
    GoodId = State()
    GoodDesc = State()

class ChangePriceGood(StatesGroup):
    GoodId = State()

class ChangeRef(StatesGroup):
    Ref = State()

class NewOrder(StatesGroup):
    Delivery = State()
    Adress = State()
    Comment = State()
    Promo = State()
    Promocode = State()

class OrderEnd(StatesGroup):
    OrderId = State()

class Rassilka(StatesGroup):
    List = State()

class RassilkaAll(StatesGroup):
    List = State()

class Withdraw(StatesGroup):
    Amount = State()
    Req = State()

class Deposit(StatesGroup):
    Amount = State()

class DeliveryAdd(StatesGroup):
    Name = State()
    EngName = State()
    Cost = State()

class DeliveryChangeName(StatesGroup):
    DeliveryId = State()
    Name = State()
    EngName = State()

class DeliveryChangeCost(StatesGroup):
    DeliveryId = State()
    Cost = State()

class ChangeToken(StatesGroup):
    Paym = State()
    Token = State()

class ChangeBalance(StatesGroup):
    UserId = State()
    Balance = State()

class ChangeRef2(StatesGroup):
    UserId = State()
    Ref = State()

class GivePromo(StatesGroup):
    UserId = State()
    Promo = State()
    Procent = State()

class GiveSkidka(StatesGroup):
    UserId = State()
    Skidka = State()

class SendMsg(StatesGroup):
    UserId = State()

class ChangeStatus(StatesGroup):
    UserId = State()

class ChangeRules(StatesGroup):
    Rules = State()

class ReviewTake(StatesGroup):
    OrderId = State()
    Stars = State()
    Review = State()

class QuestAddQuest(StatesGroup):
    CountMsg = State()
    QuestId = State()



class ChangeReviewPay(StatesGroup):
    Pay = State()

class NewUsername(StatesGroup):
    Username = State()

class ChageNicknameAdm(StatesGroup):
    UserId = State()
    Nickname = State()
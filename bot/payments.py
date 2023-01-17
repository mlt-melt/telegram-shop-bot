from pyqiwip2p import *
from yoomoney import Client, Quickpay
from config import db
import random
import string
import aiohttp


def api_crypto():
    token = db.get_token('CRYPTO')
    return token

def qiwi_private_key():
    qiwi = db.get_token('QIWI')
    return qiwi

def yoomoney_token():
    yoom = db.get_token('YOOMONEY')
    return yoom

def get_payment(user_id, id_order, amount):
    p2p = QiwiP2P(qiwi_private_key())
    if id_order != 'n':
        bill_id = f'{user_id}_{id_order}'
        paylink = p2p.bill(bill_id=bill_id, amount=amount).pay_url
    else:
        paylink = p2p.bill(amount=amount)

    
    return paylink


def check_payment(bill_id):
    p2p = QiwiP2P(qiwi_private_key())

    if p2p.check(bill_id).status == "PAID":
        return 'pay'
    else:
        return 'nopay'


async def getCoins():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.nowpayments.io/v1/merchant/coins', headers={'x-api-key': api_crypto()}) as resp:
            response = await resp.json()
            return response['selectedCurrencies']

async def createPayment(amount, paycurrency, currency):
    headers = {
        'x-api-key': api_crypto()
    }
    payload = {
        "price_amount": float(amount),
        "price_currency": currency,
        "pay_currency": paycurrency,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.nowpayments.io/v1/payment', headers=headers, data=payload) as resp:
            response = await resp.json()
            return response

async def check_pay(payment_id):
    headers = {
        'x-api-key': api_crypto()
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.nowpayments.io/v1/payment/{payment_id}', headers=headers) as resp:
            response = await resp.json()
            return response['payment_status']



def client():
    token = yoomoney_token()
    client = Client(token)
    return client

def create_pay(summ, user_id, order_id):
    if order_id != 'n':
        quickpay = Quickpay(
            receiver='КОШЕЛЕК',
            quickpay_form='shop',
            targets='sponsor',
            paymentType='SB',
            sum=summ,
            label=f'{user_id}_{order_id}'
        )
        return quickpay.redirected_url
    else:
        a = ''.join(random.choices(string.ascii_lowercase, k=6))
        quickpay = Quickpay(
            receiver='КОШЕЛЕК',
            quickpay_form='shop',
            targets='sponsor',
            paymentType='SB',
            sum=summ,
            label=f'{user_id}_{a}'
        )
        return [quickpay.redirected_url, f'{user_id}_{a}']


def check_pay_yoo(user_id, order_id, lab):
    if lab == '1':
        history = client().operation_history(label=f'{user_id}_{order_id}')
        if len(history.operations) == 0:
            return 'no'
        else:
            for operation in history.operations:
                if operation.status == 'success':
                    return 'pay'
    else:
        history = client().operation_history(label=lab)
        if len(history.operations) == 0:
            return 'no'
        else:
            for operation in history.operations:
                if operation.status == 'success':
                    return 'pay'
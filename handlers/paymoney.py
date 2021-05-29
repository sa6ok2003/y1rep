from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp, bot
import requests
import json
from random import randint
import asyncio
from .sqlit import channeg_money

QIWI_TOKEN = 'a4408e334545fe5954a4b8283060c8f3'
QIWI_ACCOUNT = '+79913541398'

@dp.callback_query_handler(text='pay_money')  # Оплата
async def profile(call: types.callback_query):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
    parameters = {'rows': '50'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments', params=parameters)
    req = json.loads(h.text)

    random_code = randint(0, 999999999)


    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🔁 Проверить', callback_data='proverka_balans')
    bat_b = types.InlineKeyboardButton(text='❌ Отменить', callback_data='otmena_balans')
    markup.add(bat_a,bat_b)
    await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=
                    '⚠️ Пополнение баланса\n\n'
                    '🥝 Оплата киви:\n\n'
                    f'👉 Номер  {QIWI_ACCOUNT}\n'
                    f'👉 Коментарий {random_code}\n'
                    '👉 Сумма  от 1 до 15000 рублей',reply_markup=markup)





@dp.callback_query_handler(text='proverka_balans')  #Проверка оплаты
async def proverka_balans(call: types.callback_query):
    text = call.message.text
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
    parameters = {'rows': '50'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments', params=parameters)
    req = json.loads(h.text)
    summa = 0
    a = 0 #ЗАМЕНА НА 0
    for i in range(len(req['data'])):
            if (str(req['data'][i]['comment']) in text) and (len(str(req['data'][i]['comment']))>3):
                try:
                    int((str(req['data'][i]['comment'])))
                    summa = req['data'][i]['sum']['amount']
                    await bot.send_message(call.message.chat.id, 'Оплата успешна. Жми /start')
                    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
                    a = 1
                except: pass

            else:
                pass
    if a == 0:
        mes = await bot.send_message(call.message.chat.id, 'Транзакция не найдена')
        await asyncio.sleep(10)
        await bot.delete_message(chat_id=call.message.chat.id,message_id=mes.message_id)

    if a == 1:
        channeg_money(call.message.chat.id,summa) #ЗАМЕНА НА summa





@dp.callback_query_handler(text='otmena_balans')  # Отмена
async def otmena_balans(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='💰 Кошельки', callback_data='walled')
    bat_b = types.InlineKeyboardButton(text='💎 Пополнить баланс', callback_data='pay_money')
    bat_c = types.InlineKeyboardButton(text='👥 Профиль', callback_data='profile')
    bat_d = types.InlineKeyboardButton(text='ℹ Информация', callback_data='info')
    markup.add(bat_a, bat_b)
    markup.row(bat_c, bat_d)
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                text='😎 Добро пожаловать в нашего бота', reply_markup=markup)
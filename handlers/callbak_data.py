from aiogram import types
from misc import dp, bot
from .sqlit import channeg_status,cheak_money
import asyncio

@dp.callback_query_handler(text_startswith='check')  # Нажал кнопку Я ПОДПИСАЛСЯ. ДЕЛАЕМ ПРОВЕРКУ
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, '⏳ Ожидайте. Идёт проверка подписки.')
    proverka1 = (await bot.get_chat_member(chat_id='@QiwiWalet_info', user_id=call.message.chat.id)).status
    if proverka1 == 'administrator' or proverka1 == 'member' or proverka1 == 'creator':
        await bot.send_message(call.message.chat.id, 'Доступ открыт. Напиши мне /start что бы продолжить')
        channeg_status(call.message.chat.id)
    else:
        await bot.send_message(call.message.chat.id, 'Доступ закрыт. Повторите попытку')


@dp.callback_query_handler(text='profile')  # Нажал кнопку Профиль
async def profile(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='💰 Кошельки', callback_data='walled')
    bat_b = types.InlineKeyboardButton(text='💎 Пополнить баланс', callback_data='pay_money')
    bat_c = types.InlineKeyboardButton(text='👥 Профиль', callback_data='profile')
    bat_d = types.InlineKeyboardButton(text='ℹ Информация', callback_data='info')
    markup.add(bat_a, bat_b)
    markup.row(bat_c, bat_d)
    money = cheak_money(call.message.chat.id)
    if 'Профиль' in call.message.text:
        pass
    else:
        await bot.edit_message_text(message_id=call.message.message_id,chat_id=call.message.chat.id, text='🧾 Профиль\n\n'
                                                                                                      f'🆔Ваш id- {call.message.chat.id}\n'
                                                                                                      f'💰Ваш баланс - {money} рублей'
                                                                                                      f'',reply_markup=markup)

@dp.callback_query_handler(text='walled')  # Нажал кнопку Кошельки
async def walled(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥇 QIWI с балансом 2400 руб | 600 руб', callback_data='qiwi_1')
    bat_b = types.InlineKeyboardButton(text='🥈 QIWI с балансом 1600 руб | 470 руб', callback_data='qiwi_2')
    bat_c = types.InlineKeyboardButton(text='🥉 QIWI с балансом 600 руб | 171 руб', callback_data='qiwi_3')
    bat_d = types.InlineKeyboardButton(text='⭐ QIWI с балансом 480 руб | 131 руб', callback_data='qiwi_4')
    bat_e = types.InlineKeyboardButton(text='НАЗАД', callback_data='walled_exit')
    markup.add(bat_a)
    markup.add(bat_b)
    markup.add(bat_c)
    markup.add(bat_d)
    markup.add(bat_e)
    await bot.edit_message_text(message_id=call.message.message_id,chat_id=call.message.chat.id,text='<b>❕ Выберите нужный товар:</b>',reply_markup=markup,parse_mode='html')

@dp.callback_query_handler(text='walled_exit')
async def walled_exit(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='💰 Кошельки', callback_data='walled')
    bat_b = types.InlineKeyboardButton(text='💎 Пополнить баланс', callback_data='pay_money')
    bat_c = types.InlineKeyboardButton(text='👥 Профиль', callback_data='profile')
    bat_d = types.InlineKeyboardButton(text='ℹ Информация', callback_data='info')
    markup.add(bat_a, bat_b)
    markup.row(bat_c, bat_d)
    await bot.edit_message_text(message_id=call.message.message_id,chat_id=call.message.chat.id,text= '😎 Добро пожаловать в нашего бота', reply_markup=markup)





@dp.callback_query_handler(text_startswith='qiwi') # Нажал на какой либо кошелек
async def qiwi_walled(call: types.callback_query):
    qiwi_number = int(call.data[5:])
    money = cheak_money(call.message.chat.id)


    if int(money) <= 131:
        if qiwi_number == 1: #Первый киви кошелек
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_1')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a,bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>🥇 QIWI с балансом 2400 руб | 600 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 600 ₽.\n'
                                             '💰 Баланс кошелька: 2400 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 600 рублей\n'
                                             '💠 Кол-во товара: 39',reply_markup=markup,parse_mode='html')

        elif qiwi_number == 2:
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_2')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a, bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>🥈 QIWI с балансом 1600 руб | 470 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 470₽.\n'
                                             '💰 Баланс кошелька: 1600 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 470 рублей\n'
                                             '💠 Кол-во товара: 20', reply_markup=markup, parse_mode='html')

        elif qiwi_number == 3:
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_3')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a, bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>🥈 QIWI с балансом 600 руб | 171 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 171₽.\n'
                                             '💰 Баланс кошелька: 600 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 171 рублей\n'
                                             '💠 Кол-во товара: 27', reply_markup=markup, parse_mode='html')

        else:
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_4')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a, bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>⭐ QIWI с балансом 480 руб | 131 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 131₽.\n'
                                             '💰 Баланс кошелька: 480 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 131 рублей\n'
                                             '💠 Кол-во товара: 7', reply_markup=markup, parse_mode='html')

    elif int(money) <= 4700: # денег меньше 4700
        markup1 = types.InlineKeyboardMarkup()
        bat_b = types.InlineKeyboardButton(text='ВЫБРАТЬ ДРУГОЙ ТИП', callback_data='exit_qiwi')
        markup1.add(bat_b)

        if qiwi_number == 1: #Первый киви кошелек
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_1')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a, bat_b)
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_1')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a,bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>🥇 QIWI с балансом 2400 руб | 600 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 600 ₽.\n'
                                             '💰 Баланс кошелька: 2400 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 600 рублей\n'
                                             '💠 Кол-во товара: 12',reply_markup=markup,parse_mode='html')

        elif qiwi_number == 2:
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_2')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a, bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>🥈 QIWI с балансом 1600 руб | 470 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 470₽.\n'
                                             '💰 Баланс кошелька: 1600 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 470 рублей\n'
                                             '💠 Кол-во товара: 18', reply_markup=markup, parse_mode='html')

        elif qiwi_number == 3:
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_3')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a, bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>🥈 QIWI с балансом 600 руб | 171 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 171₽.\n'
                                             '💰 Баланс кошелька: 600 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 171 рублей\n'
                                             '<b>💠 Кол-во товара: нет в наличии</b>', reply_markup=markup1, parse_mode='html')

        else:
            markup = types.InlineKeyboardMarkup()
            bat_a = types.InlineKeyboardButton(text='Купить', callback_data='buy_qiwi_4')
            bat_b = types.InlineKeyboardButton(text='Выйти', callback_data='exit_qiwi')
            markup.add(bat_a, bat_b)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Вы выбрали :\n'
                                             '<b>⭐ QIWI с балансом 480 руб | 131 руб</b>\n\n'
                                             '🔸 Qiwi кошелёк, цена: 131₽.\n'
                                             '💰 Баланс кошелька: 480 руб\n\n'
                                             '▪При покупки кошелька, вы получаете: логин, пароль\n\n'
                                             '☑️Смс код выключен!\n\n'
                                             '💠 Цена: 131 рублей\n'
                                             '<b>💠 Кол-во товара: нет в наличии</b>', reply_markup=markup1, parse_mode='html')

@dp.callback_query_handler(text='exit_qiwi') # Нажал выйти после покупки
async def exit_qiwi(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥇 QIWI с балансом 2400 руб | 600 руб', callback_data='qiwi_1')
    bat_b = types.InlineKeyboardButton(text='🥈 QIWI с балансом 1600 руб | 470 руб', callback_data='qiwi_2')
    bat_c = types.InlineKeyboardButton(text='🥉 QIWI с балансом 600 руб | 171 руб', callback_data='qiwi_3')
    bat_d = types.InlineKeyboardButton(text='⭐ QIWI с балансом 480 руб | 131 руб', callback_data='qiwi_4')
    bat_e = types.InlineKeyboardButton(text='НАЗАД', callback_data='walled_exit')
    markup.add(bat_a)
    markup.add(bat_b)
    markup.add(bat_c)
    markup.add(bat_d)
    markup.add(bat_e)
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                text='<b>❕ Выберите нужный товар:</b>', reply_markup=markup, parse_mode='html')


@dp.callback_query_handler(text_startswith='buy_qiwi') # Нажал Заплатить
async def bue_qiwi(call: types.callback_query):
    number = int(call.data[9:])
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ЗАПЛАТИТЬ', callback_data='ready')
    bat_b = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otmena')
    markup.add(bat_a,bat_b)
    if number == 1:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Вы выбрали:\n'
                                         '🥇 QIWI с балансом 2400 руб | 600 руб:\n\n'
                                         '💠 Цена: 600 рублей\n'
                                         'Для подтверждения покупки, нажимай кнопку👇', reply_markup=markup)
    elif number == 2:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Вы выбрали:\n'
                                         '🥈 QIWI с балансом 1600 руб | 470 руб:\n\n'
                                         '💠 Цена: 470 рублей\n'
                                         'Для подтверждения покупки, нажимай кнопку👇', reply_markup=markup)

    elif number == 3:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Вы выбрали:\n'
                                         '🥈 QIWI с балансом 600 руб | 171 руб:\n\n'
                                         '💠 Цена: 171 рублей\n'
                                         'Для подтверждения покупки, нажимай кнопку👇', reply_markup=markup)
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Вы выбрали:\n'
                                         '⭐ QIWI с балансом 480 руб | 131 руб\n\n'
                                         '💠 Цена: 131 рублей\n'
                                         'Для подтверждения покупки, нажимай кнопку👇', reply_markup=markup)

@dp.callback_query_handler(text='ready')
async def ready(call: types.callback_query):
    money = cheak_money(call.message.chat.id)
    a = await bot.send_message(call.message.chat.id, '❌ Недостаточно средств\n'
                                                     f'<b>⭐ На вашем счете: {money} рублей</b>\n\n',parse_mode='html')
    await asyncio.sleep(20)
    await bot.delete_message(chat_id=call.message.chat.id,message_id=a.message_id)


@dp.callback_query_handler(text='otmena')
async def otmena(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥇 QIWI с балансом 2400 руб | 600 руб', callback_data='qiwi_1')
    bat_b = types.InlineKeyboardButton(text='🥈 QIWI с балансом 1600 руб | 470 руб', callback_data='qiwi_2')
    bat_c = types.InlineKeyboardButton(text='🥉 QIWI с балансом 600 руб | 171 руб', callback_data='qiwi_3')
    bat_d = types.InlineKeyboardButton(text='⭐ QIWI с балансом 480 руб | 131 руб', callback_data='qiwi_4')
    bat_e = types.InlineKeyboardButton(text='НАЗАД', callback_data='walled_exit')
    markup.add(bat_a)
    markup.add(bat_b)
    markup.add(bat_c)
    markup.add(bat_d)
    markup.add(bat_e)
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                text='<b>❕ Выберите нужный товар:</b>', reply_markup=markup, parse_mode='html')
from aiogram import types
from misc import dp,bot
from .sqlit import reg_user,cheak_status
import asyncio


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    z = message.text[7:]
    if (len(z)) == 0:
        reg_user(message.chat.id,refka=0)
    else:
        reg_user(message.chat.id,refka=z)
    a = cheak_status(message.chat.id)
    if a == 1:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='💰 Кошельки', callback_data='walled')
        bat_b = types.InlineKeyboardButton(text='💎 Пополнить баланс', callback_data='pay_money')
        bat_c = types.InlineKeyboardButton(text='👥 Профиль', callback_data='profile')
        bat_d = types.InlineKeyboardButton(text='ℹ Информация', callback_data='info')
        markup.add(bat_a, bat_b)
        markup.row(bat_c, bat_d)
        await bot.send_message(message.chat.id,'😎 Добро пожаловать в нашего бота',reply_markup=markup)

    else:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='🔺Я ПОДПИСАЛСЯ🔺', callback_data= 'check')
        markup.add(bat_a)
        await bot.send_message(message.chat.id, f'📌 Для продолжения работы с ботом вступите в наш <b>INFO канал:</b>@QiwiWalet_info\n\n'
                                                f'✅ После подписки нажми кнопку <b>Я ПОДПИСАЛСЯ</b>',parse_mode='html',reply_markup=markup)
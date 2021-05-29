from aiogram import types
from misc import dp, bot
import sqlite3
import asyncio

from .sqlit import members_list,add_urlmetka,info_metki,dannie_metki
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 =  1307813926

ADMIN_ID =[ADMIN_ID_1]

class trek_reg(StatesGroup):
    trek_name = State()
    trek_fname = State()


class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()



@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        bat_setin = types.InlineKeyboardButton(text='Настройка рефералок', callback_data='settings')
        markup.add(bat_a,bat_e,bat_j)
        markup.add(bat_setin)
        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)


########################################################### НАСТРОЙКА ТРЕКЕРА
@dp.callback_query_handler(text='settings')
async def settings_trek(call: types.callback_query):
    markup1 = types.InlineKeyboardMarkup()
    bat_1 = types.InlineKeyboardButton(text='Регистрация новой ссылки', callback_data='fgdfkjk')
    bat_3 = types.InlineKeyboardButton(text='Список всех меток', callback_data='list_metok')
    bat_2 = types.InlineKeyboardButton(text='Назад', callback_data='exit1')
    markup1.add(bat_1)
    markup1.add(bat_3)
    markup1.add(bat_2)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text='Панель управления рефералками',reply_markup=markup1)


#Просмотр всех меток
@dp.callback_query_handler(text='list_metok',state='*')
async def cheak_metki(call: types.callback_query, state: FSMContext):
    metki = info_metki()
    for i in metki:
        dann = dannie_metki(i[0])
        await bot.send_message(chat_id=call.message.chat.id, text=f'<b>Метка:</b> https://t.me/QiwiWall_bot?start={i[0]}\n'
                                                                  f'<b>Описание:</b> {i[1]}\n\n'
                                                                  f'<b>Количество трафика: {dann[0]}</b>\n'
                                                                  f'<b>Заработано денег</b>: {dann[1]}',parse_mode='html')
        await asyncio.sleep(1)

# НАСТРОЙКА Метки
@dp.callback_query_handler(text='exit1',state='*')
async def otmena_vsego(call: types.callback_query, state: FSMContext):
    try: await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    except: pass
    await bot.send_message(call.message.chat.id,text='ОТМЕНЕНО')
    await state.finish()


@dp.callback_query_handler(text='fgdfkjk')
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправь метку')
    await trek_reg.trek_name.set()

@dp.message_handler(state=trek_reg.trek_name,content_types=['text']) # Текст Метки
async def trek_get_metka(message: types.Message, state: FSMContext):
    await state.update_data(url_m=message.text)  # Занесение в сет url метки
    await bot.send_message(chat_id=message.chat.id,text='Отправь описание к метке')
    await trek_reg.trek_fname.set()

@dp.message_handler(state=trek_reg.trek_fname,content_types=['text']) # Описание Метки
async def trek_get_opisanie_metka(message: types.Message, state: FSMContext):
    await state.update_data(text_m=message.text)  # Занесение в сет описания url метки

    markup_met = types.InlineKeyboardMarkup()
    bat_11 = types.InlineKeyboardButton(text='Зарегистрировать', callback_data='reg_metka')
    bat_22 = types.InlineKeyboardButton(text='Отмена', callback_data='exit1')
    markup_met.add(bat_11)
    markup_met.add(bat_22)

    data = await state.get_data()
    metka_url = data['url_m']

    await bot.send_message(message.chat.id, text=f'<b>Метка:</b> {metka_url}\n\n'
                                                 f'<b>Описание:</b> {message.text}',reply_markup=markup_met,parse_mode='html')


@dp.callback_query_handler(text='reg_metka',state=trek_reg.trek_fname)
async def reg_metka(call: types.callback_query, state: FSMContext):
    data = await state.get_data()
    metka_url = data['url_m']
    text_m = data['text_m']
    add_urlmetka(metka_url,text_m) # Регистрация в бд метки
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id, text='Метка зарегистрирована')
    await state.finish()



######################
@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    a = open('server.db','rb')
    await bot.send_document(chat_id=call.message.chat.id, document=a)


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    a = members_list() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot\n\n'
                                                     'Пока можно добавить только одну кнопку')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################
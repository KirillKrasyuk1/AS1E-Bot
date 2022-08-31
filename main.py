# import telebot
from aiogram import Bot, Dispatcher, executor, types
import time
import requests
from bs4 import BeautifulSoup as BS
import schedule
import sqlite3
import asyncio
import aioschedule
from database import Database


bot = Bot('5502855452:AAEDWiH4cF6PQHaVMPV0hOY5cC-9zLhuY5E')
database = Database(file_db='db.db')
dp = Dispatcher(bot)
#TODO менять времябез попадания в функцию answer
@dp.message_handler(commands=['settings'])
async def settings(message):
    global button2
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'рассылка с погодой'
    button2 = 'рыссылка с курсом валют'
    keyboard.add(button1, button2)
    await bot.send_message(message.chat.id, 'Выберете ту функцию которую хотите изменить.')


@dp.message_handler(commands=['start'])
async def greeting(message):
    if database.is_user_exist(user_id= message.chat.id) == False:
        database.add_user(user_id=message.chat.id)

    # us_id = message.from_user.id
    # username = message.from_user.username
    # db_table_val(user_id=us_id, username=username)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'погода'
    button2 = 'курс валют'
    # button3 = 'быстроновости'
    keyboard.add(button1, button2)
    await bot.send_message(message.from_user.id,
                     str(message.from_user.id) + 'Привет, я твой умный помощник AS1E! Я умею показывать погоду на сегодня, курс валют и быстроновости.'
                     ' Выбери что из этого ты хочешь получать каждый день. P.S. чтобы увидеть список команд напиши /help.',
                     reply_markup=keyboard)


@dp.message_handler(content_types=['text'])
async def answer(message):
    if message.text == 'погода':
        await bot.send_message(message.chat.id, 'Напииште название свего города через восклицательный знак')
    if message.text[0] == '!':
        city = message.text[1:].lower()
        print(city)
        database.add_city(city=city, user_id=message.chat.id)
        await bot.send_message(message.chat.id, 'Введите время в которое хотите получать рассылку.')
    if message.text[2] == ':':
        t = message.text + ':00'
        await bot.send_message(message.chat.id, 'Отлично!')
        database.add_time(time=t, user_id=message.chat.id)

# тестирование таймера
async def weather(city, chat_id):
    # chat_id = 1759119378
    response = requests.get(f'https://sinoptik.ua/погода-{city}')
    html_response = BS(response.content, 'html.parser')
    a = html_response.find('div', id='bd1')
    if a == None:
        await bot.send_message(chat_id, 'Такого города не существует или его название написано неправильно')
    else:
        a = a.select('.temperature')[0].text
        await bot.send_message(chat_id, a)

async def mailing(t, city, chat_id):
    aioschedule.every().day.at(t).do(weather, city=city, chat_id=chat_id)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(t, city, chat_id):
    asyncio.create_task(mailing(t, city, chat_id))


while True:
    t = '18:07'
    city = 'самара'
    chat_id = 1759119378
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup(t, city, chat_id))
    time.sleep(5)
# @bot.message_handler(content_types=['text'])
# async def valutes(message):
#     if button2 == 'курс валют':
#         bot.send_message(message.chat.id, 'Отлично, теперь я буду присылать тебе курс основых валют')
# bot.send_message(message.chat.id, 'Хочешь воспользоваться другими моими функциями')


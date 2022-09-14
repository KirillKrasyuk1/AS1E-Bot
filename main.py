
from aiogram import Bot, Dispatcher, executor, types
import time
import schedule
import sqlite3
import asyncio
import aioschedule
from database import Database
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from WeatherForTheBot import parsing_weather

sched = AsyncIOScheduler()
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
                     'Привет, я твой умный помощник AS1E! Я умею показывать погоду на сегодня, курс валют и быстроновости.'
                     ' Выбери что из этого ты хочешь получать каждый день. P.S. чтобы увидеть список команд напиши /help.',
                     reply_markup=keyboard)
#TODO разбить время на часы минуты секунды и вставить в декоратор(50 сточка)


@dp.message_handler(content_types=['text'])
async def ansswer(message):
    if message.text == 'погода':
        await bot.send_message(message.chat.id, 'Напииште название свего города через восклицательный знак')
    if message.text[0] == '!':
        city = message.text[1:].lower()
        parsing_try = parsing_weather(city=city)
        if parsing_try != None:
            database.add_city(city=city, user_id=message.chat.id)
            await bot.send_message(message.chat.id, 'Введите время в которое хотите получать рассылку. Например чч:мм')
        else:
            await bot.send_message(message.chat.id, 'Такого города не существует или вы ввели его название с ошибкой. Попробуйте еще раз.')
    if message.text[2] == ':':
        t = message.text + ':00'
        database.add_time(time=t, user_id=message.chat.id)
        await bot.send_message(message.chat.id, 'Отлично!')
        await mailing(message)
async def mailing(message):
    time, city = database.get_time_and_city(user_id=message.from_user.id)[0]
    hour = time[:2]
    minute = time[3:5]
    @sched.scheduled_job(trigger='cron', day='*', hour=hour, minute=minute, second='00', id=str(message.from_user.id))
    async def timed_job():
        weather_str = parsing_weather(city=city)
        await bot.send_message(message.chat.id, weather_str)

    sched.start()


#TODO здесь я удалил погоду
executor.start_polling(dp, skip_updates=False)
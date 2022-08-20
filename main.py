import telebot
import time
import requests
from bs4 import BeautifulSoup as BS
import schedule


bot = telebot.TeleBot('5502855452:AAEDWiH4cF6PQHaVMPV0hOY5cC-9zLhuY5E')
#TODO менять времябез попадания в функцию answer
@bot.message_handler(commands=['settings'])
def settings(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'рассылка с погодой'
    button2 = 'рыссылка с курсом валют'
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберете ту функцию которую хотите изменить.')


@bot.message_handler(commands=['start'])
def greeting(message):

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = 'погода'
    button2 = 'курс валют'
    # button3 = 'быстроновости'
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id,
                     'Привет, я твой умный помощник AS1E! Я умею показывать погоду на сегодня, курс валют и быстроновости.'
                     ' Выбери что из этого ты хочешь получать каждый день. P.S. чтобы увидеть список команд напиши /help.',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def answer(message):
    global id_to_test
    id_to_test = message.chat.id
    if message.text == 'погода':
        bot.send_message(message.chat.id, 'Напииште название свего города через восклицательный знак')
    if message.text[0] == '!':
        Text = message.text
        city = Text[1:]
        bot.send_message(message.chat.id, 'Отлично, я запомню. Теперь я буду присылать прогноз погоды в 18:20')
        response = requests.get(f'https://sinoptik.ua/погода-{city.lower()}')
        html_response = BS(response.content, 'html.parser')
        a = html_response.find('div', id='bd1')
        if a == None:
            bot.send_message(message.chat.id, 'Такого города не существует или его название написано неправильно')
        else:
            a = a.select('.temperature')[0].text
            bot.send_message(message.chat.id, a)

# тестирование таймера
def weather():
    city = 'самара'
    # ставлю свой id для теста 
    chat_id = 494790051
    response = requests.get(f'https://sinoptik.ua/погода-{city.lower()}')
    html_response = BS(response.content, 'html.parser')
    a = html_response.find('div', id='bd1')
    if a == None:
        bot.send_message(chat_id, 'Такого города не существует или его название написано неправильно')
    else:
        a = a.select('.temperature')[0].text
        bot.send_message(chat_id, a)

# обоварачиваем режим ожидания в функцию, чтобы запустить в отдельном потоке  
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("18:39").do(weather)
# сначала запуск в отдельном потоке, потом ожидание бота. В обратном порядке не работает
Thread(target=schedule_checker).start()
bot.polling()


# if button2 == 'курс валют':
#     bot.send_message(message.chat.id, 'Отлично, теперь я буду присылать тебе курс основых валют')
# bot.send_message(message.chat.id, 'Хочешь воспользоваться другими моими функциями')


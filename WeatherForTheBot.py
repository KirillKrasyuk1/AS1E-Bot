from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup as BS
def parsing_weather(city):
    try:
        response = requests.get(f'https://sinoptik.ua/погода-{city}')
        html_response = BS(response.content, 'html.parser')
        a = html_response.find('div', id='bd1')
        a = a.select('.temperature')[0].text
        print(a)
        return a
    except:
        return None



# async def mailing(t, city, chat_id):
#     aioschedule.every().day.at(t).do(weather, city=city, chat_id=chat_id)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)

# async def on_startup(t, city, chat_id):
#     asyncio.create_task(mailing(t, city, chat_id))

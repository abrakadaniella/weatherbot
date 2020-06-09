import telebot
import requests
import json
from config import token

bot = telebot.TeleBot(token)


markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
itembtn1 = telebot.types.KeyboardButton('Share Location', request_location=True)
markup.add(itembtn1)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """Greetings, {}!
I am a Weather Bot!
If you don't mind sharing location, press the button and I'll tell you the weather at your location.
Otherwise enter name of a city.""".format(message.chat.first_name), reply_markup=markup)

  
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, """Currently supported commands:
/start - begins communication with the bot
/help - this is what you just did

If you share location, the bot will return the weather at your current location.
If you want to know the weather at some city, type only the name of the city, country name is not needed.""")
    

@bot.message_handler(content_types=["location"])
def location_btn(message):
    url = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=e395731afdbc105951e43d2d535427bf".format(message.location.latitude, message.location.longitude))
    content = url.content
    js = json.loads(content)
    cur_weather = js['weather'][0]['main']
    description = js['weather'][0]['description']
    temperature_c = round(float(js['main']['temp']) - 273.15, 2)
    humidity = '{}%'.format(js['main']['humidity'])
    wind_speed = '{} m/s'.format(js['wind']['speed']) 
    city_name = js['name']
    bot.send_message(message.chat.id, """Current weather at {city}:
{weath} ({desc})
Temperature: {temp}
Air humidity: {hum}
Wind speed: {wind}""".format(city = city_name, temp = temperature_c, hum = humidity, wind = wind_speed, weath = cur_weather, desc = description))
    
cat_cities = ['Betya', 'Motya', 'Begemot', 'Motilda', 'Leonid', 'Debil', 'Matilda', 'Lyonya']

@bot.message_handler(content_types=['text'])
def city_weather(message):
    if message.text not in cat_cities:
        url = requests.get("https://api.openweathermap.org/data/2.5/weather?q={}&appid=e395731afdbc105951e43d2d535427bf".format(message.text))
        content = url.content
        js = json.loads(content)
        if js['cod'] != 200:
            bot.send_message(message.chat.id, "I don't know such city, please check your request for mistakes or try another name.")
        else:
            cur_weather = js['weather'][0]['main']
            description = js['weather'][0]['description']
            temperature_c = round(float(js['main']['temp']) - 273.15, 2)
            humidity = '{}%'.format(js['main']['humidity'])
            wind_speed = '{} m/s'.format(js['wind']['speed']) 
            city_name = message.text
            bot.send_message(message.chat.id, """Current weather at {city}:
{weath} ({desc})
Temperature: {temp}
Air humidity: {hum}
Wind speed: {wind}""".format(city = city_name, temp = temperature_c, hum = humidity, wind = wind_speed, weath = cur_weather, desc = description))
    elif message.text in cat_cities:
        url = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Nur-Sultan&appid=e395731afdbc105951e43d2d535427bf")
        content = url.content
        js = json.loads(content)
        cur_weather = js['weather'][0]['main']
        description = js['weather'][0]['description']
        temperature_c = round(float(js['main']['temp']) - 273.15, 2)
        humidity = '{}%'.format(js['main']['humidity'])
        wind_speed = '{} m/s'.format(js['wind']['speed']) 
        city_name = message.text
        bot.send_message(message.chat.id, """Current weather at {city}:
{weath} ({desc})
Temperature: {temp}
Air humidity: {hum}
Wind speed: {wind}""".format(city = city_name, temp = temperature_c, hum = humidity, wind = wind_speed, weath = cur_weather, desc = description))
    
    
bot.polling(timeout = 0.5)
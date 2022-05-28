import requests, settings
from emoji import emojize
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup([['Send a cat', KeyboardButton('Send my location', request_location=True)]])


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Your number is {user_number}, mine is {bot_number}, you won!'
    elif user_number == bot_number:
        message = f'Your number is {user_number}, mine is {bot_number}, that`s a draw!'
    else:
        message = f'Your number is {user_number}, mine is {bot_number}, You lost!'
    return message


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']


def get_weather_by_city(city_name):
    weather_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params = {
        'key': settings.WEATHER_KEY,
        'q': city_name,
        'format': 'json',
        'num_of_days': '1',
    }
    result = requests.get(weather_url, params=params)
    weather = result.json()
    if 'data' in weather:
        if 'current_condition' in weather['data']:
            try:
                return weather['data']['current_condition'][0]
            except(IndexError, TypeError):
                return False
    return False

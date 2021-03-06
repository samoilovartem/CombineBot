import ephem
import datetime
from glob import glob
from utils import main_keyboard, play_random_numbers, get_bot_number, get_weather_by_city, \
     get_object, cat_rating_inline_keyboard
from db import db, get_or_create_user, subscribe_user, unsubscribe_user, save_cate_image_vote, \
    find_if_user_voted, get_image_rating
import os
from telegram import ParseMode
from random import choice
from jobs import alarm


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    update.message.reply_text(
        f'Hello, {user["first_name"]}! {user["emoji"]}',
        reply_markup=main_keyboard()
    )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    text = update.message.text
    update.message.reply_text(
        f'{text} {user["emoji"]}',
        reply_markup=main_keyboard()
    )


def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    if context.args:
        try:
            user_number = int(context.args[0])
            bot_number = get_bot_number(user_number)
            message = play_random_numbers(user_number, bot_number)
        except (TypeError, ValueError):
            message = 'Enter a whole number please'
    else:
        message = 'Enter a number please'
    update.message.reply_text(
        f'{message} {user["emoji"]}',
        reply_markup=main_keyboard()
    )


def send_cat_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    cat_photo_list = glob('images/cat_*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    if find_if_user_voted(db, cat_photo_filename, user['user_id']):
        rating = get_image_rating(db, cat_photo_filename)
        keyboard = None
        caption = f'This picture`s rating is {rating}'
    else:
        keyboard = cat_rating_inline_keyboard(cat_photo_filename)
        caption = None
    context.bot.send_photo(chat_id=chat_id,
                           photo=open(cat_photo_filename, 'rb'),
                           reply_markup=keyboard,
                           caption=caption)


def get_weather(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    city = context.args[0]
    weather = get_weather_by_city(city)
    if weather:
        update.message.reply_text(
            f'Weather in {city}: {weather["temp_C"]}, '
            f'feels like {weather["FeelsLikeC"]} {user["emoji"]}',
            reply_markup=main_keyboard())
    else:
        return update.message.reply_text(
            'Weather service is temporary unavailable',
            reply_markup=main_keyboard())


def words_count(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    words = context.args
    words_count = len(words)
    update.message.reply_text(
        f'Your text has {words_count} words {user["emoji"]}',
        reply_markup=main_keyboard())


def next_full_moon(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    today = datetime.datetime.now()
    next_full_moon = ephem.next_full_moon(today).datetime().strftime(
        '%b %d, %Y at %H:%M:%S'
        )
    update.message.reply_text(f'Next full moon will be on {next_full_moon}',
                              reply_markup=main_keyboard())


def calculator(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_context = context.args
    if user_context:
        user_input = user_context[0]
        if '-' in user_input:
            user_input = list(map(int, user_input.split('-')))
            result = user_input[0] - user_input[1]
            update.message.reply_text(result, reply_markup=main_keyboard())
        elif '+' in user_input:
            user_input = list(map(int, user_input.split('+')))
            result = user_input[0] + user_input[1]
            update.message.reply_text(result, reply_markup=main_keyboard())
        elif '*' in user_input:
            user_input = list(map(int, user_input.split('*')))
            result = user_input[0] * user_input[1]
            update.message.reply_text(result, reply_markup=main_keyboard())
        elif '/' in user_input:
            try:
                user_input = list(map(int, user_input.split('/')))
                result = user_input[0] / user_input[1]
                update.message.reply_text(result, reply_markup=main_keyboard())
            except ZeroDivisionError:
                update.message.reply_text(
                    'You can`t divide by zero, illiterate!',
                    reply_markup=main_keyboard())
    else:
        update.message.reply_text(
            'Please follow the format: \n/calc 2*3\n/calc 10-3 \netc',
            reply_markup=main_keyboard())


def get_user_location(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    coordinates = update.message.location
    update.message.reply_text(
        f'Your coordinates are: \nLatitude - {coordinates["latitude"]} '
        f'\nLongitude - {coordinates["longitude"]} \n{user["emoji"]}',
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    update.message.reply_text('Your picture has been received \n'
                              'Please wait while I`m analyzing it')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join(
        'downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    user_list = '\n'.join(get_object(file_name)[0:5])
    if user_list:
        update.message.reply_text(
            'Here is what I have found in your picture: ' + user_list,
            parse_mode=ParseMode.HTML)
        if 'cat' in user_list:
            update.message.reply_text(
                f'Since it`s a cat, I`ll save this picture to my library! '
                f'Thank you, {user["username"]} :)')
            new_file_name = os.path.join(
                'images', f'cat_{photo_file.file_id}.jpg')
            os.rename(file_name, new_file_name)
        else:
            os.remove(file_name)
    else:
        update.message.reply_text(
            f'Unfortunately, I`m not sure what objects are in this picture. '
            f'Sorry, {user["first_name"]}')


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('You have successfully subscribed')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('You have successfully unsubscribed')


def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f'You will get an alarm in {alarm_seconds} seconds')
    except (ValueError, TypeError):
        update.message.reply_text(
            'Enter amount of seconds after the command.\n'
            'Example: /alarm 100')


def rate_cate_picture(update, context):
    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split('|')
    vote = int(vote)
    user = get_or_create_user(db, update.effective_user,
                              update.effective_chat.id)
    save_cate_image_vote(db, user, image_name, vote)
    rating = get_image_rating(db, image_name)
    update.callback_query.edit_message_caption(caption=f'Picture`s rating is {rating}')


def get_city(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_context = context.args

    if user_context:
        used_cities_list = context.user_data.get("used_cities")
        if used_cities_list is None:
            used_cities_list = used_cities
            context.user_data["used_cities"] = used_cities

        bot_cities = context.user_data.get("cities")
        if bot_cities is None:
            bot_cities = cities
            context.user_data["cities"] = cities

        user_city = user_context[0].capitalize()

        if user_city not in used_cities_list:
            context.user_data["used_cities"].append(user_city)

            if user_city in bot_cities:
                suitable_cities = list(filter(lambda x: x.startswith(
                    user_city[-1].upper()), bot_cities))
                if suitable_cities:
                    context.user_data["used_cities"].append(suitable_cities[0])
                    context.user_data["cities"].remove(suitable_cities[0])
                    context.user_data["cities"].remove(user_city)
                    update.message.reply_text(suitable_cities[0])
                else:
                    update.message.reply_text(
                        f'Unfortunately, I don`t know any city that starts '
                        f'from "{user_city[-1].upper()}". You won!')
            else:
                update.message.reply_text(
                    'I don`t know that city, but let`s pretend it exists!')
                suitable_cities = list(filter(lambda x: x.startswith(
                    user_city[-1].upper()), bot_cities))
                if suitable_cities:
                    update.message.reply_text(suitable_cities[0])
                    context.user_data['cities'].append(suitable_cities[0])
                    context.user_data['used_cities'].append(user_city)
                else:
                    update.message.reply_text(
                        f'Unfortunately, I don`t know any city that starts '
                        f'from "{user_city[-1].upper()}". You won!')
        else:
            update.message.reply_text(
                'We have already used that city! '
                'Don`t try to trick me, cheater!')

    else:
        update.message.reply_text('Please follow the format: \n/cities Moscow')


used_cities = []


cities = [
    'Aberdeen', 'Accra', 'Aden', 'Albany', 'Alexandria', 'Algiers', 'Alberta',
    'Amsterdam', 'Anchorage', 'Ankara', 'Antananarivo', 'Antrim', 'Antwerp',
    'Assouan', 'Athens', 'Babylon', 'Baghdad', 'Baikonur', 'Barcelona',
    'Basel', 'Belgrade', 'Berlin', 'Beijing', 'Bhilai', 'Bogota', 'Brazilia',
    'Brno', 'Brussels', 'Bucharest', 'Budapest', 'Buenos Aires', 'Bukhara',
    'Cadiz', 'Cairo', 'Calais', 'Calcutta', 'Cambridge', 'Canberra', 'Caracas',
    'Cologne', 'Copenhagen', 'Dakar', 'Damascus', 'Davos', 'Delhi', 'Dover',
    'Dublin', 'Dushanbe', 'Dusseldorf', 'Edinburgh', 'Florence', 'Geneva',
    'Glasgow', 'Greenwich', 'Guatemala', 'Hague', 'Halifax', 'Hamburg',
    'Harare', 'Harbin', 'Havana', 'Helsinki', 'Hiroshima', 'Hull', 'Iasi',
    'Istanbul', 'Jerusalem', 'Johannesburg', 'Kabul', 'Kyoto', 'Lagos',
    'Lausanne', 'Leiden', 'Leipzig', 'Lisbon', 'Ljubljana', 'London', 'Lyons',
    'Madrid', 'Manchester', 'Marseilles', 'Melbourne', 'Monaco', 'Moscow',
    'Montreal', 'Munich', 'Naples', 'Nice', 'Omaha', 'Orlando', 'Orleans',
    'Osaka', 'Oslo', 'Ottawa', 'Padua', 'Phoenix', 'Plymouth', 'Portsmouth',
    'Prague', 'Pyongyang', 'Quebec', 'Richmond', 'Rome', 'Sachalin',
    'Salvador', 'Seoul', 'Seville', 'Shanghai', 'Sicily', 'Sofia', 'Stockholm',
    'Strasbourg', 'Suez', 'Sydney', 'Syracuse', 'Taipei', 'Toulouse', 'Tunis',
    'Valparaiso', 'Vancouver', 'Venice', 'Versailles', 'Vienna', 'Vilnuis',
    'Warsaw', 'Warwick', 'Weimar', 'Zurich',
]

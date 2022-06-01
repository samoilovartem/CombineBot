import ephem, datetime
from glob import glob
from utils import *
import os


def greet_user(update, context):
    username = update.effective_user.first_name
    update.message.reply_text(
        f'Hello {username}! {get_smile(context.user_data)}',
        reply_markup=main_keyboard()
    )


def talk_to_me(update, context):
    text = update.message.text
    update.message.reply_text(
        f"{text} {get_smile(context.user_data)}",
        reply_markup=main_keyboard()
    )


def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Enter a whole number please'
    else:
        message = 'Enter a number please'
    update.message.reply_text(
        f'{message} {get_smile(context.user_data)}',
        reply_markup=main_keyboard()
    )


def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat_*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id,
                           photo=open(cat_photo_filename, 'rb'),
                           reply_markup=main_keyboard())


def get_weather(update, context):
    city = context.args[0]
    weather = get_weather_by_city(city)
    if weather:
        update.message.reply_text(
            f"Weather in {city}: {weather['temp_C']}, "
            f"feels like {weather['FeelsLikeC']} {get_smile(context.user_data)}",
            reply_markup=main_keyboard())
    else:
        return update.message.reply_text('Weather service is temporary unavailable',
                                         reply_markup=main_keyboard())


def words_count(update, context):
    words = context.args
    words_count = len(words)
    update.message.reply_text(f'Your text has {words_count} words {get_smile(context.user_data)}',
                              reply_markup=main_keyboard())


def next_full_moon(update, context):
    today = datetime.datetime.now()
    next_full_moon = ephem.next_full_moon(today).datetime().strftime('%b %d, %Y at %H:%M:%S')
    update.message.reply_text(f'Next full moon will be on {next_full_moon}',
                              reply_markup=main_keyboard())


def calculator(update, context):
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
                update.message.reply_text('You can`t divide by zero, illiterate!',
                                          reply_markup=main_keyboard())
    else:
        update.message.reply_text('Please follow the format: \n/calc 2*3\n/calc 10-3 \netc',
                                  reply_markup=main_keyboard())


def get_user_location(update, context):
    coordinates = update.message.location
    update.message.reply_text(
        f'Your coordinates are: \nLatitude - {coordinates["latitude"]} '
        f'\nLongitude - {coordinates["longitude"]} \n{get_smile(context.user_data)}',
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    update.message.reply_text('Your photo is processing')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Your file has been saved')
    if has_object(file_name, 'cat'):
        update.message.reply_text('Kitty cat has been detected! Saving it into our library :)')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Attention! A cat hasn`t been detected')


def get_city(update, context):
    username = update.effective_user.first_name
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
                suitable_cities = list(filter(lambda x: x.startswith(user_city[-1].upper()), bot_cities))
                if suitable_cities:
                    context.user_data["used_cities"].append(suitable_cities[0])
                    context.user_data["cities"].remove(suitable_cities[0])
                    context.user_data["cities"].remove(user_city)
                    update.message.reply_text(suitable_cities[0])
                    print(f'{used_cities_list} for {username}')
                    print(f'{context.user_data["used_cities"]} for {username}')

                else:
                    update.message.reply_text(
                        f'Unfortunately, I don`t know any city that starts from "{user_city[-1].upper()}". You won!')
            else:
                update.message.reply_text('I don`t know that city, but let`s pretend it exists!')
                suitable_cities = list(filter(lambda x: x.startswith(user_city[-1].upper()), bot_cities))
                if suitable_cities:
                    update.message.reply_text(suitable_cities[0])
                    context.user_data['cities'].append(suitable_cities[0])
                    context.user_data['used_cities'].append(user_city)
                    print(used_cities_list)
                else:
                    update.message.reply_text(
                        f'Unfortunately, I don`t know any city that starts from "{user_city[-1].upper()}". You won!')
        else:
            update.message.reply_text('We have already used that city! Don`t try to trick me, cheater!')

    else:
        update.message.reply_text('Please follow the format: \n/cities Moscow')



used_cities = []


cities = [
    'Aberdeen', 'Accra', 'Aden', 'Albany', 'Alexandria', 'Algiers', 'Alberta', 'Amsterdam',
    'Anchorage', 'Ankara', 'Antananarivo', 'Antrim', 'Antwerp', 'Assouan', 'Athens', 'Babylon',
    'Baghdad', 'Baikonur', 'Barcelona', 'Basel', 'Belgrade', 'Berlin', 'Beijing', 'Bhilai',
    'Bogota', 'Brazilia', 'Brno', 'Brussels', 'Bucharest', 'Budapest', 'Buenos Aires', 'Bukhara',
    'Cadiz', 'Cairo', 'Calais', 'Calcutta', 'Cambridge', 'Canberra', 'Caracas', 'Cologne',
    'Copenhagen', 'Dakar', 'Damascus', 'Davos', 'Delhi', 'Dover', 'Dublin', 'Dushanbe',
    'Dusseldorf', 'Edinburgh', 'Florence', 'Geneva', 'Glasgow', 'Greenwich', 'Guatemala',
    'Hague', 'Halifax', 'Hamburg', 'Harare', 'Harbin', 'Havana', 'Helsinki', 'Hiroshima',
    'Hull', 'Iasi', 'Istanbul', 'Jerusalem', 'Johannesburg', 'Kabul', 'Kyoto', 'Lagos',
    'Lausanne', 'Leiden', 'Leipzig', 'Lisbon', 'Ljubljana', 'London', 'Lyons', 'Madrid',
    'Manchester', 'Marseilles', 'Melbourne', 'Monaco', 'Moscow', 'Montreal', 'Munich', 'Naples',
    'Nice', 'Omaha', 'Orlando', 'Orleans', 'Osaka', 'Oslo', 'Ottawa', 'Padua', 'Phoenix',
    'Plymouth', 'Portsmouth', 'Prague', 'Pyongyang', 'Quebec', 'Richmond', 'Rome', 'Sachalin',
    'Salvador', 'Seoul', 'Seville', 'Shanghai', 'Sicily', 'Sofia', 'Stockholm',
    'Strasbourg', 'Suez', 'Sydney', 'Syracuse', 'Taipei', 'Toulouse', 'Tunis', 'Valparaiso',
    'Vancouver', 'Venice', 'Versailles', 'Vienna', 'Vilnuis', 'Warsaw', 'Warwick',
    'Weimar', 'Zurich',
]

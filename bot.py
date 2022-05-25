from glob import glob
import ephem, requests, settings, logging, datetime
from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, choice


logging.basicConfig(filename='bot.log', level=logging.INFO)


# ************** BOT FUNCTIONS *************** #
def greet_user(update, context):
	print(update)
	smile = context.user_data['emoji'] = get_smile(context.user_data)
	update.message.reply_text(f'Hello User! {smile}')

def talk_to_me(update, context):
	text = update.message.text
	print(text)
	smile = context.user_data['emoji'] = get_smile(context.user_data)
	update.message.reply_text(f"{text} {smile}")

def guess_number(update, context):
	smile = context.user_data['emoji'] = get_smile(context.user_data)
	print(context.args)
	if context.args:
		try:
			user_number = int(context.args[0])
			message = play_random_numbers(user_number)
		except (TypeError, ValueError):
			message = 'Enter a whole number please'
	else:
		message = 'Enter a number please'
	update.message.reply_text(f'{message} {smile}')

def send_cat_picture(update, context):
	cat_photo_list = glob('images/cat_*.jp*g')
	cat_photo_filename = choice(cat_photo_list)
	chat_id = update.effective_chat.id
	context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))

def get_weather(update, context):
	smile = context.user_data['emoji'] = get_smile(context.user_data)
	print(context.args)
	city = context.args[0]
	weather = weather_by_city(city)
	if weather:
		update.message.reply_text(f"Weather in {city}: {weather['temp_C']}, feels like {weather['FeelsLikeC']} {smile}")
	else:
		return update.message.reply_text('Weather service is temporary unavailable')

def words_count(update, context):
	smile = context.user_data['emoji'] = get_smile(context.user_data)
	words = context.args
	words_count = len(words)
	update.message.reply_text(f'Your text has {words_count} words {smile}')

def next_full_moon(update, context):
	today = datetime.datetime.now()
	next_full_moon = ephem.next_full_moon(today).datetime().strftime('%b %d, %Y at %H:%M:%S')
	update.message.reply_text(f'Next full moon will be on {next_full_moon}')
	print(type(ephem.next_full_moon(today)))




# ************* ADDITIONAL FUNCTIONS ************** #

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


def weather_by_city(city_name):
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

# def rock_paper_scissors():
# 	while True:
# 		choices = ['rock', 'paper', 'scissors']
# 		computer = choice(choices)
# 		player = None
#
# 		while player not in choices:
# 			player = input('rock, paper or scissors?: ').lower()
# 		if player == computer:
# 			print('Computer:', computer)
# 			print('Player:', player)
# 			print('Tie!')
# 		elif player == 'rock':
# 			if computer == 'paper':
# 				print('Computer:', computer)
# 				print('Player:', player)
# 				print('You lose!')
# 			if computer == 'scissors':
# 				print('Computer:', computer)
# 				print('Player:', player)
# 				print('You win!')
# 		elif player == 'scissors':
# 			if computer == 'rock':
# 				print('Computer:', computer)
# 				print('Player:', player)
# 				print('You lose!')
# 			if computer == 'paper':
# 				print('Computer:', computer)
# 				print('Player:', player)
# 				print('You win!')
# 		elif player == 'paper':
# 			if computer == 'scissors':
# 				print('Computer:', computer)
# 				print('Player:', player)
# 				print('You lose!')
# 			if computer == 'rock':
# 				print('Computer:', computer)
# 				print('Player:', player)
# 				print('You win!')
#
# 		play_again = input("Play again? (yes/no): ").lower()
# 		if play_again != 'yes':
# 			break
# 	print('Bye!')

def main():
	mybot = Updater(settings.API_KEY, use_context=True)

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler('start', greet_user))
	dp.add_handler(CommandHandler('guess', guess_number))
	dp.add_handler(CommandHandler('cat', send_cat_picture))
	dp.add_handler(CommandHandler('weather', get_weather))
	dp.add_handler(CommandHandler('wordscount', words_count))
	dp.add_handler(CommandHandler('next_full_moon', next_full_moon))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))


	logging.info('The bot has started')
	mybot.start_polling()
	mybot.idle()


if __name__ == '__main__':
	main()



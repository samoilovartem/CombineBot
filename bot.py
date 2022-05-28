from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from handlers import *

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('weather', get_weather))
    dp.add_handler(CommandHandler('wordscount', words_count))
    dp.add_handler(CommandHandler('next_full_moon', next_full_moon))
    dp.add_handler(CommandHandler('calc', calculator))
    dp.add_handler(CommandHandler('cities', get_city))
    dp.add_handler(MessageHandler(Filters.regex('^(Send a cat)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, get_user_location))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('The bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()

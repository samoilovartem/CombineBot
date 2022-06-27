from datetime import time
from telegram.ext.jobqueue import Days
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
     ConversationHandler
from telegram.bot import Bot
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request
import logging
import pytz
import settings

from handlers import greet_user, talk_to_me, guess_number, send_cat_picture, \
     get_weather, words_count, next_full_moon, calculator, get_user_location, \
     check_user_photo, get_city, subscribe, unsubscribe, set_alarm
from form import form_start, form_name, form_rating, form_skip, form_comment, \
     form_unknown
from jobs import send_updates


logging.basicConfig(filename='bot.log', level=logging.INFO)


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)


def main():
    request = Request(
        con_pool_size=8,
    )
    bot = MQBot(settings.API_KEY, request=request)

    mybot = Updater(bot=bot, use_context=True)

    jq = mybot.job_queue
    target_time = time(12, 0, tzinfo=pytz.timezone('Asia/Manila'))
    target_days = (Days.MON, Days.WED, Days.FRI)
    jq.run_daily(send_updates, target_time, target_days)

    dp = mybot.dispatcher

    form = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Fill out the form)$'), form_start)
        ],
        states={
            'name': [MessageHandler(Filters.text, form_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'),
                       form_rating)],
            'comment': [
                CommandHandler('skip', form_skip),
                MessageHandler(Filters.text, form_comment),
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.sticker |
                           Filters.video | Filters.document | Filters.location,
                           form_unknown)
        ],
    )

    dp.add_handler(form)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('weather', get_weather))
    dp.add_handler(CommandHandler('wordscount', words_count))
    dp.add_handler(CommandHandler('next_full_moon', next_full_moon))
    dp.add_handler(CommandHandler('calc', calculator))
    dp.add_handler(CommandHandler('cities', get_city))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('alarm', set_alarm))
    dp.add_handler(MessageHandler(Filters.regex('^(Send a cat)$'),
                                  send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, get_user_location))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('The bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()

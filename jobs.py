from datetime import datetime
from db import db, get_subscribed
from telegram.error import BadRequest


def send_updates(context):
    now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    for user in get_subscribed(db):
        try:
            context.bot.send_message(chat_id=user['chat_id'], text=f'Exact time is: {now}')
        except BadRequest:
            print(f"Chat {user['chat_id']} not found")


def alarm(context):
    context.bot.send_message(chat_id=context.job.context, text='ALARM!!!')
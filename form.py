from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from utils import main_keyboard
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, save_form


def form_start(update, context):
    update.message.reply_text(
        'Hello! What`s your name?',
        reply_markup=ReplyKeyboardRemove(),
    )
    return 'name'


def form_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Please enter your First name and Last name')
        return 'name'
    else:
        context.user_data['form'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        update.message.reply_text(
            'Please rate our bot on a scale '
            'from 1 (very bad) to 5 (very good)',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                             one_time_keyboard=True)
        )
        return 'rating'


def form_rating(update, context):
    context.user_data['form']['rating'] = int(update.message.text)
    update.message.reply_text('Please leave a comment or press /skip')
    return 'comment'


def form_comment(update, context):
    context.user_data['form']['comment'] = update.message.text
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id)
    save_form(db, user['user_id'], context.user_data['form'])
    user_text = form_format(context.user_data['form'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def form_skip(update, context):
    user = get_or_create_user(
        db, update.effective_user, update.message.chat.id)
    save_form(db, user['user_id'], context.user_data['form'])
    user_text = form_format(context.user_data['form'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def form_format(form):
    user_text = f'''<b>Full name</b>: {form['name']}
<b>Rating</b>: {form['rating']}
'''
    if 'comment' in form:
        user_text += f"<b>Comment</b>: {form['comment']}"
    return user_text


def form_unknown(update, context):
    update.message.reply_text('Unfortunately, I don`t understand you :(')

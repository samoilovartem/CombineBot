from datetime import datetime
from pymongo import MongoClient
from random import choice
from emoji import emojize
import settings
import certifi

client = MongoClient(settings.MONGO_URI, tlsCAFile=certifi.where())

db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "emoji": emojize(choice(settings.USER_EMOJI), use_aliases=True)
        }
        db.users.insert_one(user)
    return user


def save_form(db, user_id, form_data):
    user = db.users.find_one({"user_id": user_id})
    form_data['created'] = datetime.now()
    if 'form' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'form': [form_data]}},
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'form': form_data}},
        )


def subscribe_user(db, user):
    if not user.get('subscribed'):
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'subscribed': True}}
        )


def unsubscribe_user(db, user):
    db.users.update_one(
        {'_id': user['_id']},
        {'$set': {'subscribed': False}}
    )


def get_subscribed(db):
    return db.users.find({"subscribed": True})


def save_cate_image_vote(db, user_data, image_name, vote):
    image = db.images.find_one({'image_name': image_name})
    if not image:
        image = {
            'image_name': image_name,
            'votes': [
                {'user_id': user_data['user_id'],
                 'vote': vote}
            ]
        }
        db.images.insert_one(image)
    elif not find_if_user_voted(db, image_name, user_data['user_id']):
        db.images.update_one(
            {"image_name": image_name},
            {'$push': {'votes': {'user_id': user_data['user_id'],
                                 'vote': vote}}}
        )


def find_if_user_voted(db, image_name, user_id):
    if db.images.find_one(
            {'image_name': image_name,
             'votes.user_id': user_id}
    ):
        return True
    return False


def get_image_rating(db, image_name):
    rating = db.images.aggregate(
        [
            {'$match': {'image_name': image_name}},
            {'$unwind': {'path': '$votes'}},
            {'$group': {'_id': '$image_name',
                        'rating': {'$sum': '$votes.vote'}}}
        ]
    )
    rating = next(rating, None)
    if rating:
        return rating['rating']
    return 0

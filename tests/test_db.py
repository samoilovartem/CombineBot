from db import find_if_user_voted, get_image_rating, get_or_create_user


def test_find_if_user_voted_true(mongodb):
    assert find_if_user_voted(mongodb, "images/cat_1.jpg", 7028155) is True


def test_find_if_user_voted_false(mongodb):
    assert find_if_user_voted(mongodb, "images/cat_1.jpg", 1) is False


def test_get_image_rating(mongodb):
    assert get_image_rating(mongodb, "images/cat_5.jpg") == 1
    assert get_image_rating(mongodb, "no_image") == 0


def test_get_or_create_user(mongodb, effective_user):
    user_exists = mongodb.users.find_one({'user_id': effective_user.id})
    assert user_exists is None
    user = get_or_create_user(mongodb, effective_user, 123)
    user_exists = mongodb.users.find_one({'user_id': effective_user.id})
    assert user == user_exists

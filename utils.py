import requests, settings
from emoji import emojize
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2


def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Send a cat', KeyboardButton('Send my location', request_location=True)],
            ['Fill out the form'],
        ]
    )


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


def get_object(filename):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    with open(filename, 'rb') as file:
        file_data = file.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_response_for_object(response)


def check_response_for_object(response):
    all_findings = dict()
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.value >= 0.97:
                all_findings[concept.name] = str(round(concept.value * 100, 1))
        return all_findings

    else:
        print(f'Picture recognition error {response.outputs[0].status.details}')
        return False


if __name__ == '__main__':
    print(get_object('images/cat_1.jpg'))


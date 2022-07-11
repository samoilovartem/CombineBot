# "CombineBot" Project

CombineBot is a bot for Telegram that I use for learning purposes. Here I add as many features as I can in order for me to test them and remember the path I`ve done. 

### Current features:
- **Greeting user** _(yeah, he knows your name but not only that...)_
- **Echo bot** _(basically sends you back whatever you text him)_
- **Guess number game** _(just send him some number and let`s see if you can win the bot)_
- **Sending pictures of cute cats** _(what can be better than that right?)_
- **Weather service** _(you will not forget to take your umbrella with this bro)_
- **Words counting** _(just counts how many words you texted him in one message. Why? Because it can)_
- **Next full moon date** _(this little bro will not judge you for that)_
- **Simple calculator** _(works with 2 digits only for now, but maybe in future this bot will be a bit worse than Pythagoras)_
- **Location** _(you don`t need to use your sextant anymore)_
- **Word chain game** _(you don`t have any chances to win that beast)_
- **Bot`s rating form** _(you can tell me if you like it and leave a review)_
- **Picture`s uploading tool** _(the bot can accept and save pictures that you sent)_
- **Object`s recognition** _(the bot can tell what objects are in a picture you sent)_
- **Subscribe and unsubscribe functionality** _(does nothing except changing "subscribed" status in Mongo to True or False)_
- **Alarm** _(can be useful sometimes to count time)_
- **Exact time notification** _(if ever you forget what time is it now this little bot will remind you about it every Monday, Wednesday and Friday)_
- **Rating system for bot`s pictures of cats** _(you just rate a picture and bot will show you current rating of it)_
- **To be continued...**


### Installation 

1. Clone the repository from GitHub
2. Create a virtual environment
3. Install requirements: `pip install requirements.txt`
4. Create a file `settings.py`
5. Fill it out:
```
API_KEY = 'Your telegram bot API key'
USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']
WEATHER_KEY = 'Your weather service api key'
CLARIFAI_API_KEY = 'Your clarifai API key'
MONGO_URI = 'Your Mongo DB URI'
MONGO_DB = 'Your DB name'
```
6. Start the bot: `python bot.py`

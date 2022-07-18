# import files and give access to tokens and keys
import tweepy
import pandas as pd
import time
import json
import sys
import csv
from pyowm.owm import OWM
from textblob import TextBlob

TWITTER_ACCESS_TOKEN = '1449432052495958022-AdDlldx3p4anKH7EPiGwbh34CyB7Sx'
TWITTER_ACCESS_TOKEN_SECRET = 'fqLcHfsr9hTWmbOgdNYWfeJ3lH0nR5ThTXBSpqcmvOHFJ'
TWITTER_CONSUMER_KEY = 'OxzmAILFV6CYdWLuVBBFZTk4n'
TWITTER_CONSUMER_SECRET = 'tKeW8FSLH7VoqCdLDWQU7eqVkhmylrFUrHBdGJW5lXgkUfvtKh'

APIKEY = '3a7810c48a0c9f7c3c38754e4415f7d7'

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

RUNTIME = 60    # Seconds to run code
weatherUpdateInterval = 30    # Seconds to update weather information

res = []


class StdOutListener(tweepy.Stream):
    def on_status(self, status):
        try:
            lang = status.lang
            text = atRemover(status.text)
            if lang == 'en' and len(text.split()) > 3:
                sentimentAnalyzer = TextBlob(text).sentiment
                sent = {'Polarity': sentimentAnalyzer[0], 'Subjectivity': sentimentAnalyzer[1]}               
                
                dateCreated = status.created_at
                box = [v for v in status.place.bounding_box.coordinates[0]]
                msg = {'Date': dateCreated, 'Text': text, 'Box': box}
                weatherCond = {'Status': weather_status, 'Temperature': temperature, 'Wind': wind}
                msg.update(weatherCond)
                msg.update(sent)
                if len(msg) == 8:
                    res.append(msg)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)


def countdown(t, mgr, weatherUpdateInterval):
    global weather_status
    global temperature
    global wind
    
    for i in range(t, -1, -1):
        if (t - i) % weatherUpdateInterval == 0:
            weather = mgr.weather_at_place('New York').weather
            weather_status = weather.status
            temperature = weather.temperature('celsius')['temp']
            wind = weather.wind()['speed']
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining...".format(i))
        sys.stdout.flush()
        time.sleep(1)
    print()


def atRemover(text):
    words = text.split()
    while words[0][0] == '@':
        words.pop(0)
    return ' '.join(words)


if __name__ == "__main__":
    print("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  threaded=True)
    
    owm = OWM(APIKEY)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('New York').weather
    
    countdown(RUNTIME, mgr, weatherUpdateInterval)
    stream.disconnect()
    #print(res)
    with open ('tweets2.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Date','Text','Box', 'Status', 'Temperature', 'Wind', 'Polarity', 'Subjectivity'],
                                lineterminator = '\n')
        writer.writeheader()
        for data in res:
            writer.writerow(data)


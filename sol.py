######################### LIBRARIES #########################
import requests # manage rest api
import string # working with strings
import re # more features involving strings
from os import environ # help heroku use credentials
import tweepy # TWITTER INTEGRATION

##### hardcoded values
expected_lyrics_length = 140
range_lyrics_length = 10

##### GENERATING GET REQUEST
base_url = 'https://api.lyrics.ovh/v1/'
band = 'tool/'
song = 'fear inoculum'

def getLyrics():
    try:
        resp = requests.get(base_url+band+song)
        # MANAGING RESPONSE
        if resp.status_code != 200:
            print('GET tasks status: {}'.format(resp.status_code))
        else:
            raw_lyrics = re.split('[\r\n]',resp.json()['lyrics']) # from json lyrics remove all \r and \n to get strings list
            lyrics = [raw_lyrics_element for raw_lyrics_element in raw_lyrics if raw_lyrics_element] # remove blank string
            lyrica = '"' # starting point
            for i in range(range_lyrics_length):
                if len(lyrica) > expected_lyrics_length or len(lyrica) + len(lyrics[i]) > expected_lyrics_length:
                    break # keep in check length in order to not
                else:
                    lyrica += lyrics[i] + '\n'
            lyricus = lyrica.rstrip() + '"\n' # ending point
            return lyricus
    except Exception as e:
        print("getLyrics - The following exception was catched: " + str(e))

def getArtistAndSong():
    try:
        artist = string.capwords(band.replace('/',''))
        songTitle = string.capwords(song)
        return artist + ' - ' + songTitle
    except Exception as e:
        print("getSongAndArtist - The following exception was catched: " + str(e))

def getHashtags():
    return '#lyrics'

def callTwitter(main_message):
    ##### GENERATING TWITTER REQUEST
    # Credentials
    CONSUMER_KEY = environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = environ['TWITTER_CONSUMER_SECRET']
    ACCESS_KEY = environ['TWIITER_ACCESS_KEY']
    ACCESS_SECRET = environ['TWITTER_ACCESS_SECRET']
    # Authenticate to Twitter: via environment variables
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    api = tweepy.API(auth)
    try:
        if api.verify_credentials() == False:
            print("The user credentials are invalid.")
        else:
            print("The user credentials are valid.")
            api.update_status(main_message)
    except tweepy.error.TweepError as e:
        print("callTwitter - The following exception was catched: " + str(e))
        errorcode = str(e.api_code)
        print("Error code: " + errorcode)
    except Exception as e:
        print("callTwitter - The following exception was catched: " + str(e))
        print("Breaking from loop. Better luck next time.")

####### main method
try:
    lyrica = getLyrics()
    authorAndSong = getArtistAndSong()
    hashtags = getHashtags()
    message = lyrica + '\n' + authorAndSong + '\n' + hashtags
    print(message)
    callTwitter(message)
except Exception as e:
    print("main - The following exception was catched: " + str(e))

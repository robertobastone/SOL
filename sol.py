######################### LIBRARIES #########################
import requests # manage rest api
import string # working with strings
import re # more features involving strings
from os import environ # help heroku use credentials
import tweepy # twitter integration

##### hardcoded values
expected_lyrics_length = 200

##### GENERATING GET REQUEST
base_url = 'https://api.lyrics.ovh/v1/'
band = 'tool' + '/'
song = 'parabola'
##### GENERATING 2ND GET REQUEST
base_wikiurl = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles='
end_wikiurl = '_(song)'

def getLyrics():
    try:
        resp = requests.get(base_url+band+song)
        # MANAGING RESPONSE
        if resp.status_code != 200:
            print('GET tasks status: {}'.format(resp.status_code))
        else:
            raw_lyrics = re.split('[\r\n]',resp.json()['lyrics']) # from json lyrics remove all \r and \n to get strings list
            lyrics = [raw_lyrics_element for raw_lyrics_element in raw_lyrics if raw_lyrics_element] # remove blank strings
            lyrica = '"' # starting point
            for i in range(len(lyrics)):
                if (len(lyrica) + len(lyrics[i])) > expected_lyrics_length:
                    break # keep in check length in order to not
                else:
                    lyrica += lyrics[i] + '\n'
            lyricus = lyrica.rstrip() + '"\n' # remove last \n + ending point
            return lyricus
    except Exception as e:
        print("getLyrics - The following exception was catched: " + str(e))

def getArtistAndSong():
    try:
        artist = string.capwords(band.replace('/','')) # capitalize band name
        songTitle = string.capwords(song) #capitalize song name
        return artist + ' - ' + songTitle
    except Exception as e:
        print("getSongAndArtist - The following exception was catched: " + str(e))

def getHashtags():
    return '#lyrics'

def generateReplyToMainTweet():
    resp = requests.get(base_wikiurl+song+end_wikiurl)
    # MANAGING RESPONSE
    if resp.status_code != 200:
       print('GET tasks status: {}'.format(resp.status_code))
    else:
       a = resp.json()

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

####### main method
try:
    lyrics = getLyrics()
    authorAndSong = getArtistAndSong()
    hashtags = getHashtags()
    message = lyrics + '\n' + authorAndSong + '\n' + hashtags
    print(message)
    callTwitter(message)
except Exception as e:
    print("main - The following exception was catched: " + str(e))

######################### LIBRARIES #########################
import requests # manage rest api
import string # working with strings
import re # more features involving strings
from os import environ # help heroku use credentials
import tweepy # twitter integration

##### hardcoded values
expected_lyrics_length = 200

##### 1ST GET REQUEST PARAMETERS
base_url = 'https://api.lyrics.ovh/v1/'
band = 'tool' + '/'
song = 'parabola'
##### 2ND GET REQUEST PARAMETERS
base_wikiurl = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&titles='
end_wikiurl = '_(song)' # assuming that all songs url on wiki end like this
wikilink = 'https://en.wikipedia.org/wiki/'

###### CREATING FIRST TWEET

#retireve lyrics
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
                    break # keep in check length in order to not exceed Twitter 280 characters limit
                else:
                    lyrica += lyrics[i] + '\n'
            lyricus = lyrica.rstrip() + '"\n' # remove last \n + ending point
            return lyricus
    except Exception as e:
        print("getLyrics - The following exception was catched: " + str(e))

# retrieve artist and song name
def getArtistAndSong():
    try:
        artist = string.capwords(band.replace('/','')) # capitalize band name
        songTitle = string.capwords(song) #capitalize song name
        return artist + ' - ' + songTitle
    except Exception as e:
        print("getSongAndArtist - The following exception was catched: " + str(e))

# retrieve hashtags
def getHashtags():
    return '#lyrics'

# gather informations and create first tweet body
def generateMainMessage():
    lyrics = getLyrics()
    authorAndSong = getArtistAndSong()
    hashtags = getHashtags()
    message = lyrics + '\n' + authorAndSong + '\n' + hashtags
    print(message)
    return message

##### CREATING SECOND TWEET (REPLY)

# get song summary from wikipedia api
def getWikiSummary():
    try:
        resp = requests.get(base_wikiurl+song+end_wikiurl)
        # MANAGING RESPONSE
        if resp.status_code != 200:
           print('GET tasks status: {}'.format(resp.status_code))
        else:
            # given the structure of the response, to access the extract we need the pageid
            keys_pages = resp.json()['query']['pages'].keys() # get keys
            pageid = list(keys_pages)[0] #from keys to list of one element, from list of one element to single id
            extract = resp.json()['query']['pages'][pageid]['extract']
            summary = extract[:expected_lyrics_length]+'...' ## keep in check length in order to not exceed Twitter 280 characters limit
            return summary
    except Exception as e:
        print("getWikiSummary - The following exception was catched: " + str(e))

# generate related wikipedia article url
def generateWikiUrl():
    wiki_redirect = wikilink+song+end_wikiurl
    print(wiki_redirect)
    return wiki_redirect

# gather informations and create second twitter body
def generateReply():
    summary = getWikiSummary()
    link = generateWikiUrl()
    reply = summary + '\n' + link
    print(reply)
    return reply

##### TWITTER INTEGRATION

def callTwitter(main_message, reply):
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
            # post first tweet about lyrics
            if(main_message != ''):
                first_tweet = api.update_status(main_message)
                # reply to this tweet
                #api.update_status('@<username> reply, first_tweet.id)
                api.update_status(status = reply, in_reply_to_status_id = first_tweet.id , auto_populate_reply_metadata=True)
            else:
                api.update_status(status = reply, in_reply_to_status_id = '1377273096546177028', auto_populate_reply_metadata=True)
    except tweepy.error.TweepError as e:
        print("callTwitter - The following exception was catched: " + str(e))
        errorcode = str(e.api_code)
        print("Error code: " + errorcode)
    except Exception as e:
        print("callTwitter - The following exception was catched: " + str(e))

####### main method
try:
    # create body first tweet
    #message = generateMainMessage()
    # api.lyrics.ovh raising error 504 - 2021/04/02
    message = ''
    # create body second one
    reply = generateReply()
    # call twitter
    callTwitter(message,reply)
except Exception as e:
    print("main - The following exception was catched: " + str(e))

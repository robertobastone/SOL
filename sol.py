######################### LIBRARIES #########################
import requests # manage rest api
import string # working with strings
import re # more features involving strings
from os import environ # help heroku use credentials
import tweepy # twitter integration

######################### STARTING CONFIGURATIONS #########################
##### hardcoded values
expected_lyrics_length = 200

##### 1ST GET REQUEST PARAMETERS
base_url = 'https://api.lyrics.ovh/v1/'
band = 'Foo Fighters' + '/'
song = 'Everlong'

##### 2ND GET REQUEST PARAMETERS
base_wikiurl = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext&titles='
end_wikiurl_1 = '_('+string.capwords(band.replace('/',''))+' song)' # wikipedia doesn't follow a standard end url for song articles
end_wikiurl_2 = '_(song)'          # sometimes it's (band+song) or (song) or nothing
end_wikiurl_3 = ''                 # one must take these three scenarios into account
wikilink = 'https://en.wikipedia.org/wiki/'

######################### CODE #########################
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
                    if "(" not in lyrics[i]:
                        lyrica += lyrics[i][0].capitalize() + lyrics[i][1:] + '\n' #capitalize only first letter of verse
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
    return message

##### CREATING SECOND TWEET (REPLY)

# try again with another end url
def tryDifferentUrl(end_wikiurl):
    if end_wikiurl == end_wikiurl_1:
        return getWikiSummary(end_wikiurl_2)
    elif end_wikiurl == end_wikiurl_2:
        return getWikiSummary(end_wikiurl_3)
    else:
        print("Can\'t find what you\'re looking for..." )

# get song summary from wikipedia api
def getWikiSummary(end_wikiurl):
    try:
        article = ""
        resp = requests.get(base_wikiurl+song+end_wikiurl)
        # managing response
        print(base_wikiurl+song+end_wikiurl)
        if resp.status_code != 200:
           print('GET tasks status: {}'.format(resp.status_code))
        else:
            # retrieve article
            pageid = list(resp.json()['query']['pages'].keys())[0] # given the structure of the response, to access the extract we need the pageid
            if pageid == "-1":
                return tryDifferentUrl(end_wikiurl)
            else:
                extract = resp.json()['query']['pages'][pageid]['extract'] # this is the whole article
                if extract != "":
                    split_extract = re.split('[\r\n]',extract) # remove \n and \r from it and splitting it
                    clean_extract = [extract_element for extract_element in split_extract if extract_element] # remove blank strings
                    for i in range(len(clean_extract)):
                        if "==" not in clean_extract[i]: # this identifies paragraph title and we can remove them
                            article += clean_extract[i] + ' '
                    summary = article[:expected_lyrics_length]+'...' ## keep in check length in order to not exceed Twitter 280 characters limit
                    return summary, end_wikiurl
                else:
                    return tryDifferentUrl(end_wikiurl)
    except Exception as e:
        print("getWikiSummary - The following exception was catched: " + str(e))

# generate related wikipedia article url
def generateWikiUrl(end_wikiurl):
    try:
        wiki_redirect = wikilink+song+end_wikiurl
        print(wiki_redirect)
        return wiki_redirect
    except Exception as e:
        print("generateWikiUrl - The following exception was catched: " + str(e))

# gather informations and create second twitter body
def generateReply():
    try:
        summary, end_wikiurl = getWikiSummary(end_wikiurl_1)
        link = generateWikiUrl(end_wikiurl)
        reply = summary + '\n' + link
        return reply
    except Exception as e:
        print("generateReply - The following exception was catched: " + str(e))

##### TWITTER INTEGRATION
def callTwitter(main_message, reply):
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
                first_tweet = api.update_status(status = main_message)
                # reply to this tweet
                api.update_status(status = reply, in_reply_to_status_id = first_tweet.id , auto_populate_reply_metadata=True)
            else:
                api.update_status(status = reply)
    except tweepy.error.TweepError as e:
        print("callTwitter - The following exception was catched: " + str(e))
        errorcode = str(e.api_code)
        print("Error code: " + errorcode)
    except Exception as e:
        print("callTwitter - The following exception was catched: " + str(e))

####### MAIN METHOD
try:
    # create body first tweet
    message = generateMainMessage()
    # create body second one
    reply = generateReply()
    # call twitter
    print('main - first message is: ' + str(message))
    print('main - second message is: ' + str(reply))
    callTwitter(message,reply)
except Exception as e:
    print("main - The following exception was catched: " + str(e))

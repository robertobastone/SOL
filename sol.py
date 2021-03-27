######################### LIBRARIES #########################
import requests # CALL GET
import re

##### hardcoded values
expected_lyrics_lenght = 140
range_lyrics_lenght = 10

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
            lyrica = '' # starting point
            for i in range(range_lyrics_length):
                if len(lyrica) > expected_lyrics_length or len(lyrica) + len(lyrics[i]) > expected_lyrics_length:
                    break # keep in check length in order to not
                else:
                    lyrica += lyrics[i] + '\n'
            return lyrica
    except Exception as e:
        print("getLyrics - The following exception was catched: " + str(e))



####### main method
try:
    lyrica = getLyrics()
    song = getSong()
    print(lyrica)
    print(song)
except Exception as e:
    print("main - The following exception was catched: " + str(e))

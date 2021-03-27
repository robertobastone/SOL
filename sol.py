######################### LIBRARIES #########################
import requests # CALL GET

##### GENERATING GET REQUEST
base_url = 'https://api.lyrics.ovh/v1/'
band = 'Breaking Benjamin/'
song = 'Firefly'

try:
    resp = requests.get(base_url+band+song)
    # MANAGING RESPONSE
    if resp.status_code != 200:
        print('GET tasks status: {}'.format(resp.status_code))
    else:
        #print('GET tasks status {}'.format(resp.status_code))
        lyrics = resp.json()['lyrics']
        print(lyrics)
except Exception as e:
    print("main - The following exception was catched: " + str(e))

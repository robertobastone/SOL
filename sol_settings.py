##################################
# this file is created to simplify the management of the informations
# needed to make the code work without having to modify the main file itself

# manage maximum length of lyrics
max_lyrics_length = 200

##### 1ST GET REQUEST PARAMETERS
base_url = 'https://api.lyrics.ovh/v1/'
band = 'Radiohead' + '/'
song = 'Reckoner' # if a song starts with 'the', write it as 'The'

##### 2ND GET REQUEST PARAMETERS
list_words_to_keep_lowercase = ['of','the','with','on','for','a','in']

# must adapt text format for wikipedia api and url generate methods
def rewriteTextAccordingToWikipediaStandard(text):
    text_words = text.split(' ')
    wiki_format = ''
    for i in range(len(text_words)):
        if text_words[i] not in list_words_to_keep_lowercase:
            wiki_format += text_words[i].capitalize() + "_"
        else:
            wiki_format += text_words[i] + "_"
    return wiki_format.rstrip("_")

band_wikiformat = rewriteTextAccordingToWikipediaStandard(band.replace('/',''))
song_wikiformat = rewriteTextAccordingToWikipediaStandard(song)

base_wikiurl = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext&titles='
end_wikiurl_1 = '_('+band_wikiformat+'_song)' # wikipedia doesn't follow a standard end url for song articles
end_wikiurl_2 = '_(song)'          # sometimes it's (band+song) or (song) or nothing
end_wikiurl_3 = ''                 # one must take these three scenarios into account
wikilink = 'https://en.wikipedia.org/wiki/'

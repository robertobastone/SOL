# SOL
SOng Lyrics (SOL) is a little script that retrieves the first <i>n</i> verses of a given song (whose title is hardcoded). This value is determined accordingly to the length of the verses, i.e. the total number of the characters in these <i>n</i> verses cannot be greater than a value (hardcoded as well). The lyrics are retrieved via the service provided by 
<a href="https://lyricsovh.docs.apiary.io/#">lyricsovh</a>, whose team I would like to thank.

After it retrieves the lyrics, it will tweet on the twitter account, whose credentials are retrieved from the environ package, through the package <b>tweepy</b>

# Milestones
1. March, 27 2021: SOL 1.00
   - minimally functioning code
2. March, 27 2021: DADBot 1.01
   - FP version

# Versions
## Version 1.00 (March, 27 2021)
- first complete version
## Version 1.01 (March, 21 2021)
- configuring heroku and twitter integration
## Version 1.02 (March, 28 2021)
- improving overall flow


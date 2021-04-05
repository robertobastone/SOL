# SOL
SOng Lyrics (SOL) is a little script that retrieves the first <i>n</i> verses of a given song (whose title is hardcoded). This value is determined accordingly to the length of the verses, i.e. the total number of the characters in these <i>n</i> verses cannot be greater than a value (hardcoded as well). The lyrics are retrieved via the service provided by
<a href="https://lyricsovh.docs.apiary.io/#">lyricsovh</a>, whose team I would like to thank.

After it retrieves the lyrics, it will tweet on the twitter account, whose credentials are retrieved from the <b>environ</b> package, through the package <b>tweepy</b>

Afterwards it will attach a reply to the tweet, whose body will be the first <i>m</i> characters of the Wikipedia song article and also the link to the before-mentioned article. The extract of the paragraph is retrieved via <a href="https://en.wikipedia.org/w/api.php">Wikipedia api</a>.

# Milestones
1. March, 27 2021: SOL 1.00
   - minimally functioning code
2. March, 27 2021: SOL 1.01
   - FP version

# Versions
## Version 1.00 (March, 27 2021)
- first complete version
## Version 1.01 (March, 21 2021)
- configuring heroku and twitter integration
## Version 1.02 (March, 28 2021)
- improving overall flows
## Version 1.03 (April, 2 2021)
- adding reply functionality
## Version 1.04 (April, 2 2021)
- adding more safety checks to correctly call <a href="https://en.wikipedia.org/w/api.php">Wikipedia api</a>.
## Version 1.05 (April, 3 2021)
- fix: code capable of correctly writing urls accordingly to wikipedia format.
## Version 1.05 (April, 5 2021)
- Manage infos like author and urls in separate file ("sol_settings.py") to easily change them, thus preventing from introducing errors in main file, and "percent-encode"  song name before writing corresponding url

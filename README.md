#About:

This is a simple bot to automate checking the weather to a Twitter account.
It is a fork of the code *Is-It-Raining*, by **John Olson**
(https://github.com/jso0003auburn).
I made this so I could run his code in a simple Raspberry Pi, instead of the Google
Cloud. I also needed to translate it to my language, which is Brazilian Portuguese.

Easy install guide
------------------

To get keys, create a new Twitter app here: https://apps.twitter.com/app/new

Now get the location you want to use here: http://woeid.rosselliot.co.nz/

on the directory you wish to install:

    wget https://raw.githubusercontent.com/ericoporto/Chove-Agora/master/install.sh
	bash install.sh

That's it. If you configured correctly, it's working! Now keep this computer on!

To remove cron entries (uninstall): `bash install.sh uninstall`.

# Details on how it works

Both main functions can be scheduled via Cron (using `crontab -e`). Remember the
folders shown here must match to where you've placed the files - using `git clone`.

###1 - A forecast tweet.

The forecast tweet will post a tweet in the following format:

	Agora: yes/no + random comment
	Mais tarde: forecasted conditions
	Hoje: Low - High
	No momento: Current Temp

The forecast is expected to run in the morning and later in the day:

    0 6,18 * * * cd /home/Chove-Agora/ && /usr/bin/python /home/Chove-Agora/tweetforecast.py


###2 - A function that continually checks if it has started raining.

This function is expected to run every 5 minutes and will only update when trainsitioning
from not raining to raining weather.

    */5 * * * * cd /home/Chove-Agora/ && /usr/bin/python /home/Chove-Agora/tweetyesrain.py

Example account updated by this script: https://twitter.com/ChuvaEmCampinas

The original John Olson script updates the twitter: https://twitter.com/IsItRainingATL

Author: Erico Vieira Porto


#Dependencies:

tweepy (https://github.com/tweepy/tweepy)

requests (https://github.com/kennethreitz/requests)

requests-oauthlib (https://github.com/requests/requests-oauthlib)

### Web dependencies

Twitter API: https://dev.twitter.com/

Yahoo Weather: https://developer.yahoo.com/weather/documentation.html



#Configuration:

Configuration is controlled through settings.cfg which must be in the same
directory as `weathertwitter.py`.  Your Twitter Application ID tokens need to be
stored in this file to give the script permission to post status messages
on your Twitter account. This section is required.

You need to create a new [app](https://apps.twitter.com/) in twitter for it to work or use valid credentials.
To create a new one, go here: https://apps.twitter.com/app/new .

The location of the Weather data is controlled by Yahoo! WOEID which is also
stored in `settings.cfg`.

You can lookup WOEID for a location here:

http://woeid.rosselliot.co.nz/


Example settings.cfg
--------------------

	[auth]
	WOEID = 455828
	CONSUMER_KEY = ConsumerKey
	CONSUMER_SECRET = ConsumerSecret
	ACCESS_TOKEN = AccessToken
	ACCESS_TOKEN_SECRET = AccessSecret



#Installing

If you don't want to use the script, you can do a manual install. It's simple and
 you get to understand how it works.

To install you must first install the dependencies and clone the code:

    sudo pip install requests
    sudo pip install requests-oauthlib
    sudo pip install tweepy
	git clone https://github.com/ericoporto/Chove-Agora.git

Then you need to configure the script and schedule the jobs using Cron.

#Logging:

The script uses the python logging, more information here: https://docs.python.org/2/library/logging.html .

This will log each cron to /tmp/TweetForecast.log and /tmp/TweetYes.log.

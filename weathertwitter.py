# -*- coding: utf-8 -*-
import logging
import sys
import tweepy
import ConfigParser
import urllib
import xml.etree.ElementTree as ET
import random
import time
import datetime

from tweepy.auth import OAuthHandler
from tweepy.api import API
from ConfigParser import NoSectionError, NoOptionError
from urllib2 import urlopen, URLError

import ywcc

def str_to_bool(s):
    ss = s.split()
    if ss[0] == 'True' or ss[0] == 'true':
         return True
    elif ss[0] == 'False' or ss[0] == 'false':
         return False
    else:
         raise -1

#settings.cfg contains WOEID for city identification as well as the keys to the Twitter API
config = ConfigParser.RawConfigParser()
config.read('settings.cfg')

#get language
lang = ywcc.tolocstr(config.get('localization', 'LANGUAGE'))
ywcc_lang = ywcc.ywcc[lang]

#is fahrenheit or celsius
unit = ywcc.totempstr(config.get('localization', 'UNIT'))

WOEID = config.get('localization', 'WOEID')

def F2Cel(fah, unit):
    if(unit=='F'):
        return fah
    elif(unit=='C'):
        return str(int((float(fah)-32.0)/1.8))
    else:
        return str(int(273+(float(fah)-32.0)/1.8))

#updates the twitter account using the codes stored in settings.cfg
def tweet(answer):
    CONSUMER_KEY = config.get('auth', 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get('auth', 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get('auth', 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get('auth', 'ACCESS_TOKEN_SECRET')

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)
    result = api.update_status(status = answer )

#	First function is designed to check the current conditions and then tweet the following
#   Now: yes/no + random comment
#   Later: forecasted conditions
#   Today: Low - High
#   Currently: Current Temp
#
#   Use Cron file to schedule

def TweetForecast():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='/tmp/TweetForecast.log')
    try:
        forecastfile = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=i")
        tree = ET.parse(forecastfile)
        root = tree.getroot()
        channel =  root[0]
        item = channel[12]
        description = item[5]
        forecast = item[7]
        high = F2Cel(forecast.attrib['high'],unit)
        low = F2Cel(forecast.attrib['low'],unit)
        forecast = ywcc_lang[str(forecast.attrib['code'])]
        currentTemp = F2Cel(description.attrib['temp'],unit)
        currentText = ywcc_lang[str(description.attrib['code'])]
        currentC = description.attrib['code']
        currentCondition = int(currentC)
        forecastfile.close()

        with open('choices/'+lang+'/tweetforecast.txt') as thetweetf:
            the_tweet = thetweetf.read().splitlines()
            thetweetf.close()
            tw_now = the_tweet[0]
            tw_later = the_tweet[1]
            tw_today = the_tweet[2]
            tw_atmoment = the_tweet[3]

        #Yahoos weather API uses certain condition codes.
        #Depending on the condition a comment on the weather will be generated.
        #comment choices can be edited in the txt files
        #If it falls within the unique codes the script just uses Yahoos own description since theyre rare enough to not be repeated often
        #Condition codes can be found at https://gist.github.com/bzerangue/805520

        rainCodes = [1,2,3,4,5,6,8,9,10,11,12,18,35,45,46]
        scatteredCodes = [37,38,39,40,47]
        fairCodes = [31,32,33,34]
        overcastCodes = [26,27,28]
        blankCodes = [29,30,44]
        snowCodes = [13,14,15,16,41,42,43,3200]
        uniqueCodes = [17,19,20,21,22,23,24,25,36]


        if currentCondition in rainCodes:
            with open('choices/'+lang+'/yeschoices.txt') as yes_choicesf:
                yes_choices = yes_choicesf.readlines()
                yes = random.choice(yes_choices)
                yes_choicesf.close()
                a = yes
                comment = str('')
        else:
            with open('choices/'+lang+'/nochoices.txt') as no_choicesf:
                no_choices = no_choicesf.readlines()
                no = random.choice(no_choices)
                no_choicesf.close()
                a = no

        if currentCondition in scatteredCodes:
            with open('choices/'+lang+'/scatteredchoices.txt') as scattered_choicesf:
                scattered_choices = scattered_choicesf.readlines()
                scattered = random.choice(scattered_choices)
                scattered_choicesf.close()
                a = scattered
                comment = str('')

        if currentCondition in fairCodes:
            with open('choices/'+lang+'/fairchoices.txt') as fair_choicesf:
                fair_choices = fair_choicesf.readlines()
                fair = random.choice(fair_choices)
                fair_choicesf.close()
                comment = fair

        if currentCondition in overcastCodes:
            with open('choices/'+lang+'/overcastchoices.txt') as overcast_choicesf:
                overcast_choices = overcast_choicesf.readlines()
                overcast = random.choice(overcast_choices)
                overcast_choicesf.close()
                comment = overcast

        if currentCondition in blankCodes:
                comment = str('')

        if currentCondition in snowCodes:
            with open('choices/'+lang+'/snowchoices.txt') as snow_choicesf:
                snow_choices = snow_choicesf.readlines()
                snow = random.choice(snow_choices)
                snow_choicesf.close()
                comment = snow


        if currentCondition in uniqueCodes:
                comment = str( ' ' + currentText + '.')


        #this is where the tweet is formatted and put together
        a = a.rstrip("\r\n")
        comment = comment.rstrip("\r\n")
        answer = (tw_now + ': ' + a + ' ' + comment + '\n' + tw_later + ': ' + forecast + '.' + '\n' + tw_today + ': ' + low + '°' + unit + ' - ' + high +'' + '°' + unit +'\n' + tw_atmoment + ': ' + currentTemp + '°' + unit)
        logging.info(answer)
        tweet(answer)

    except URLError:
        logging.error('URLError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + ', line ' + str(sys.exc_info()[2].tb_lineno))
        logging.error(answer)

    except IOError:
        logging.error('IOError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + ', line ' + str(sys.exc_info()[2].tb_lineno))
        logging.error(answer)

    except:
        logging.error('Unexpected error: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + ', line ' + str(sys.exc_info()[2].tb_lineno))
        logging.error(answer)

#Checks if it is raining or not and replies with a simple yes and the current temp
#
#This will ONLY tweet if it is raining.
# It creates a file to detect if it was previously raining and only tweet when
#trainsitioning from not raining to raining state.
#
#Use cron to run TweetYes every 5min.
#

def SetRainBool(boolToSet):
    fn = "/tmp/chove-agora.rainbool"
    with open(fn,'w') as f:
        f.write(str(bool(boolToSet)))
        f.close()

def GetRainBool():
    fn = "/tmp/chove-agora.rainbool"
    RainBoolValue = False
    try:
        with open(fn,'r') as f:
            RainBoolValue = str_to_bool(f.read())
            f.close()
    except IOError:
        with open(fn,'w') as f:
            f.write(str(bool(0)))
            RainBoolValue = str_to_bool(f.read())
            f.close()

    return RainBoolValue

def TweetYes():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='/tmp/TweetYes.log')
    try:
        forecastfile = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=i")
        tree = ET.parse(forecastfile)
        root = tree.getroot()
        channel =  root[0]
        item = channel[12]
        description = item[5]
        currentC = description.attrib['code']
        currentCondition = int(currentC)
        forecast = item[7]
        high = F2Cel(forecast.attrib['high'],unit)
        low = F2Cel(forecast.attrib['low'],unit)
        forecast = ywcc_lang[str(forecast.attrib['code'])]
        currentTemp = F2Cel(description.attrib['temp'],unit)
        currentText = ywcc_lang[str(description.attrib['code'])]
        forecastfile.close()

        rainCodes = [1,2,3,4,5,6,8,9,10,11,12,18,35,45,46,47]
        thunderCodes = [38]
        rainbool = GetRainBool()

        logging.debug('rainbool: ' + str(rainbool))

        if currentCondition in rainCodes:
            if (rainbool != True) :
                with open('choices/'+lang+'/itsraining.txt') as yes_choicesf:
                    yes_choices = yes_choicesf.readlines()
                    yes_choicesf.close()
                yes = random.choice(yes_choices)
                a = str( ' ' + yes + '\n' + currentTemp + '°' + unit)
                tweet(a)
                logging.info(a)
                time.sleep(30)
            SetRainBool(True)
            return True

        else:
            logging.debug('Ainda não está chovendo: ' + currentC + ' ' + currentText + ' ' + currentTemp)

        if currentCondition in thunderCodes:
            if (rainbool !=True) :
        		a = str( currentText + '\n' + currentTemp + '°' +unit)
        		tweet(a)
        		logging.info(a)
        		time.sleep(30)
            SetRainBool(True)
            return True

        SetRainBool(False)
        return False


    except URLError:
        logging.error('URLError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + ', line ' + str(sys.exc_info()[2].tb_lineno))

    except IOError:
        logging.error('IOError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + ', line ' + str(sys.exc_info()[2].tb_lineno))

    except:
        logging.error('Unexpected error: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + ', line ' + str(sys.exc_info()[2].tb_lineno))

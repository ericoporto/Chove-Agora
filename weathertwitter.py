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

def str_to_bool(s):
    ss = s.split()
    if ss[0] == 'True':
         return True
    elif ss[0] == 'False':
         return False
    else:
         raise -1 

ywcc_ptbr = {
    '0':  'tornado',                       # tornado
    '1':  'tempestade tropical',           # tropical storm
    '2':  'furacão',                       # hurricane
    '3':  'tempestade severa',             # severe thunderstorms
    '4':  'trovoadas',                     # thunderstorms
    '5':  'chuva e neve',                  # mixed rain and snow
    '6':  'chuva e granizo fino',          # mixed rain and sleet
    '7':  'neve e granizo fino',           # mixed snow and sleet
    '8':  'garoa gélida',                  # freezing drizzle
    '9':  'garoa',                         # drizzle
    '10': 'chuva gélida',                  # freezing rain
    '11': 'chuvisco',                      # showers
    '12': 'chuva',                         # showers
    '13': 'neve em flocos finos',          # snow flurries
    '14': 'leve precipitação de neve',     # light snow showers
    '15': 'ventos com neve',               # blowing snow
    '16': 'neve',                          # snow
    '17': 'chuva de granizo',              # hail
    '18': 'pouco granizo',                 # sleet
    '19': 'pó em suspensão',               # dust
    '20': 'neblina',                       # foggy
    '21': 'névoa seca',                    # haze
    '22': 'enfumaçado',                    # smoky
    '23': 'vendaval',                      # blustery
    '24': 'ventando',                      # windy
    '25': 'frio',                          # cold
    '26': 'nublado',                       # cloudy
    '27': 'muitas nuvens (noite)',         # mostly cloudy (night)
    '28': 'muitas nuvens (dia)',           # mostly cloudy (day)
    '29': 'parcialmente nublado (noite)',  # partly cloudy (night)
    '30': 'parcialmente nublado (dia)',    # partly cloudy (day)
    '31': 'céu limpo (noite)',             # clear (night)
    '32': 'ensolarado',                    # sunny
    '33': 'tempo bom (noite)',             # fair (night)
    '34': 'tempo bom (dia)',               # fair (day)
    '35': 'chuva e granizo',               # mixed rain and hail
    '36': 'quente',                        # hot
    '37': 'tempestades isoladas',          # isolated thunderstorms
    '38': 'tempestades esparsas',          # scattered thunderstorms
    '39': 'tempestades esparsas',          # scattered thunderstorms
    '40': 'chuvas esparsas',               # scattered showers
    '41': 'nevasca',                       # heavy snow
    '42': 'tempestades de neve esparsas',  # scattered snow showers
    '43': 'nevasca',                       # heavy snow
    '44': 'parcialmente nublado',          # partly cloudy
    '45': 'chuva com trovoadas',           # thundershowers
    '46': 'tempestade de neve',            # snow showers
    '47': 'relâmpagos e chuvas isoladas',  # isolated thundershowers
    '3200': 'não disponível'               # not available
}

#settings.cfg contains WOEID for city identification as well as the keys to the Twitter API
config = ConfigParser.RawConfigParser()
config.read('settings.cfg')
WOEID = config.get('auth', 'WOEID')

def F2Cel(fah):
    return str(int((float(fah)-32.0)/1.8))

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
    try:
        forecastfile = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=i")
        tree = ET.parse(forecastfile)
        root = tree.getroot()
        channel =  root[0]
        item = channel[12]
        description = item[5]
        forecast = item[7]
        high = F2Cel(forecast.attrib['high'])
        low = F2Cel(forecast.attrib['low'])
        forecast = ywcc_ptbr[str(forecast.attrib['code'])]
        currentTemp = F2Cel(description.attrib['temp'])
        currentText = ywcc_ptbr[str(description.attrib['code'])]
        currentC = description.attrib['code']
        currentCondition = int(currentC)
        forecastfile.close()

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
            with open('choices/yeschoices.txt') as yes_choicesf:
                yes_choices = yes_choicesf.readlines()
                yes = random.choice(yes_choices)
                yes_choicesf.close()
                a = yes
                comment = str('')
        else:
            with open('choices/nochoices.txt') as no_choicesf:
                no_choices = no_choicesf.readlines()
                no = random.choice(no_choices)
                no_choicesf.close()
                a = no

        if currentCondition in scatteredCodes:
            with open('choices/scatteredchoices.txt') as scattered_choicesf:
                scattered_choices = scattered_choicesf.readlines()
                scattered = random.choice(scattered_choices)
                scattered_choicesf.close()
                a = scattered
                comment = str('')

        if currentCondition in fairCodes:
            with open('choices/fairchoices.txt') as fair_choicesf:
                fair_choices = fair_choicesf.readlines()
                fair = random.choice(fair_choices)
                fair_choicesf.close()
                comment = fair

        if currentCondition in overcastCodes:
            with open('choices/overcastchoices.txt') as overcast_choicesf:
                overcast_choices = overcast_choicesf.readlines()
                overcast = random.choice(overcast_choices)
                overcast_choicesf.close()
                comment = overcast

        if currentCondition in blankCodes:
                comment = str('')

        if currentCondition in snowCodes:
            with open('choices/snowchoices.txt') as snow_choicesf:
                snow_choices = snow_choicesf.readlines()
                snow = random.choice(snow_choices)
                snow_choicesf.close()
                comment = snow


        if currentCondition in uniqueCodes:
                comment = str( ' ' + currentText + '.')


        #this is where the tweet is formatted and put together
        a = a.rstrip("\r\n")
        comment = comment.rstrip("\r\n")
        answer = ('Agora: ' + a + ' ' + comment + '\n' + "Mais tarde: " + forecast + '.' + '\n' + 'Hoje: ' + low + '°C - ' + high + '°C\n' + 'No momento: ' + currentTemp + '°C')
        logging.info(answer)
        tweet(answer)

    except URLError:
        logging.error('URLError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
        logging.error(answer)

    except IOError:
        logging.error('IOError: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
        logging.error(answer)

    except:
        logging.error('Unexpected error: ' + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
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
    forecastfile = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=i")
    tree = ET.parse(forecastfile)
    root = tree.getroot()
    channel =  root[0]
    item = channel[12]
    description = item[5]
    currentC = description.attrib['code']
    currentCondition = int(currentC)
    forecast = item[7]
    high = F2Cel(forecast.attrib['high'])
    low = F2Cel(forecast.attrib['low'])
    forecast = ywcc_ptbr[str(forecast.attrib['code'])]
    currentTemp = F2Cel(description.attrib['temp'])
    currentText = description.attrib['text']
    forecastfile.close()
    rainCodes = [1,2,3,4,5,6,8,9,10,11,12,18,35,45,46,47]
    thunderCodes = [38]
    if currentCondition in rainCodes:
        if (GetRainBool() != True) :
            yes_choices = ['Sim.', 'Sim.', 'Sim Sim!', "Sim...", 'Sim, chovendo...', 'Sim!!', 'Si!', 'SIM.', 'Sim, chuva.', "Sim, vai precisar de um guarda-chuva.", "Sim, estamos ouvindo chuva!"]
            yes = random.choice(yes_choices)
            a = str( ' ' + yes + '\n' + currentTemp + '°')
            tweet(a)
            logging.info(a)
            time.sleep(30)
        SetRainBool(True)
        return True

    else:
        logging.debug('Ainda não está chovendo: ' + currentC + ' ' + currentText + ' ' + currentTemp)

    if currentCondition in thunderCodes:
        if (GetRainBool()!=True) :
    		a = str( currentText + '\n' + currentTemp + '°C')
    		tweet(a)
    		logging.info(a)
    		time.sleep(30)
        SetRainBool(True)
        return True

    SetRainBool(False)
    return False

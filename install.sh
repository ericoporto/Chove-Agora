#!/bin/bash
#This script should be in folder you downloaded all the code
#run this script WITHOUT Sudo.
#it will ask your password when needed.

#install dependencies
sudo pip install requests
sudo pip install requests-oauthlib
sudo pip install tweepy

THISFOLDER=`pwd`
THISNOW=`date +"%m%d%y-%H%M%S"`

#time to configure the settings
nano  $THISFOLDER/settings.cfg

#keep a copy of current crontab
crontab -l > original.$THISNOW.cronfile

#let's make a new crontab
crontab -l > /tmp/new.cronfile

printf "\n...adding to cron...\n"
#echo new cron into cron file
echo "0 6,18 * * * cd $THISFOLDER && /usr/bin/python $THISFOLDER/tweetforecast.py"  >> /tmp/new.cronfile
echo "*/5 * * * * cd $THISFOLDER && /usr/bin/python $THISFOLDER/tweetyesrain.py"  >> /tmp/new.cronfile
echo " "  >> /tmp/new.cronfile

#install new cron file
crontab /tmp/new.cronfile

#remove new cron file
rm /tmp/new.cronfile

#say success
printf "\n\nInstalled!\n\n"

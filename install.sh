#!/bin/bash
# Run this script WITHOUT Sudo.  It will ask your password when needed.
# This script should be in folder you downloaded all the code.
# If not, it will ask to download.
#

for i in "$@" ; do
    if [[ $i == "uninstall" ]] ; then
        crontab -l | while read -r; do
            [[ $REPLY = *"tweetforecast.py"* ]] || [[ $REPLY = *"tweetyesrain.py"* ]] && continue
            printf '%s\n' "$REPLY"
        done | crontab -
        echo " "
        echo "removed entries from cron"
        echo " "
        exit
    fi
done

if [[ -f "weathertwitter.py" && -f "tweetforecast.py" && -f "tweetyesrain.py" ]];
then
    echo "File exists."
else
    echo "This folder doesn't have the needed files"
    read -r -p "Should I download the files here? [y/N] " response
    if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
    then
        git clone https://github.com/ericoporto/Chove-Agora.git
        cd Chove-Agora
    else
        echo "exiting..."
        exit
    fi
fi

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
crontab -l | while read -r; do
    [[ $REPLY = *"tweetforecast.py"* ]] || [[ $REPLY = *"tweetyesrain.py"* ]] && continue
    printf '%s\n' "$REPLY"
done | crontab -

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
printf "\nInstalled!\nkeep this computer on.\n\n"

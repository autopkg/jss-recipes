#!/bin/bash

consoleuser=$(python -c 'from SystemConfiguration import SCDynamicStoreCopyConsoleUser; import sys; username = (SCDynamicStoreCopyConsoleUser(None, None, None) or [None])[0]; username = [username,""][username in [u"loginwindow", None, u""]]; sys.stdout.write(username + "\n");')

if grep -q "$consoleuser" /Users/"$consoleuser"/Library/Application\ Support/ownCloud/owncloud.cfg
then
   echo "Already set up"_
else
    printf '%s\n' '[ownCloud]' 'authType=http' "http_user=$consoleuser"  'url=https://owncloud.yourdomain.com' "user=$consoleuser" >> /Users/"$consoleuser"/Library/Application\ Support/ownCloud/owncloud.cfg
    echo "Added user and URL details"
fi

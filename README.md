# tpLinkM4Reboot


# Install

## Pre-requisite

### Windows (10)

### Linux
#### Ubuntu
````
* sudo apt-get update
* sudo apt-get upgrade  
* sudo apt-get install python3 python3-pip firefox-esr firefox-geckodriver
* pip3 install selenium
````
#### Raspian
````
* sudo apt-get update
* suod apt-get upgrade
* sudo apt-get install python3 python3-pip firefox-esr firefox-geckodriver
* pip3 install selenium
````
## this package
--todo--
download 
or 
curl

# Usage
## commandline all OS
````
python3 tpLinkM4Reboot.py
````
## windows - taskscheduler (commandline add)

## windows - taskscheduler (ui)

## linux - cron job
assumption is that the user and home dir is /home/pi/tplink
add command to crontab
````
sudo crontab -e
````
add a line like this
````
0 3 * * * /usr/bin/python3 /home/pi/tplink/tpLinkM4Reboot.py >> /home/pi/tplink/log.log 2>&1
````
This eg. would execute the script every day at 03:00 in th enight.

Hint: https://crontab.guru will help you on creating the right time string for crontab 
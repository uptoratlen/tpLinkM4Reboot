# tpLinkM4Reboot

- [tpLinkM4Reboot](#tplinkm4reboot)
  * [Overview](#overview)
  * [Technologies](#technologies)
  * [Setup](#setup)
  * [Edit tplinkm4.json](#edit-tplinkm4json)
- [Install](#install)
  * [Pre-requisite](#pre-requisite)
    + [Windows (10)](#windows--10-)
    + [Linux](#linux)
      - [FreeBSD](#freebsd)      
      - [Ubuntu](#ubuntu)
      - [Raspian / pi 3 or 4](#raspian---pi-3-or-4)
  * [this package](#this-package)
- [Usage](#usage)
  * [commandline (linux)](#commandline--linux-)
  * [commandline (windows)](#commandline--windows-)
  * [windows - taskscheduler (commandline add)](#windows---taskscheduler--commandline-add-)
  * [linux - cron job](#linux---cron-job)
  * [logging](#logging)
- [Future](#future)

## Overview
Main purpose of this program is to overcome the missing feature of the [tp-link M4 Deco](https://www.tp-link.com/de/home-networking/deco/deco-m4/) and tp-link M5 Deco of a scheduled reboot.  
A reboot is often needed like described here: (https://community.tp-link.com/en/home/forum/topic/225858), to free the cache or increase speed.    
The web front end of the main deco got a reboot feature. So the program will use a selenium automation to click on the needed buttons/links.

What it does. Well let's demonstrate it in a video.
[Demo Video](http://www.kastaban.de/demo_mp4/tpLinkM4Reboot.mp4 "Demo Video")  
I blurred the video, but if you are familiar with the webpage, you will see what it does and how it navigates.
The video was stopped when the reboot would have been executed. But as my family would raised some concerns when I reboot the WiFi right during the day...well you admin life is hard...

The steps the automation does are:
* sign in 
* navigate to the reboot page
* wait for all devices to show up (not sure if needed, but I wait for at least one/all)
* click on reboot
* confirm reboot
More or less the same steps a user would do.

## Technologies
The tpLinkM4Reboot obviously was created in Python with Selenium and the geckodriver(firefox) and or chromedriver (Chrome)-
I used to test with firefox but in case you prefer chromium, that should be no big deal (see install, but currently missing)
The browser runs also headless, that means it will run with no visible window.

```
* The job ran successful with web pages at 17th March 2021.
* Python 3.7.3 (also 3.9.2 also worked)
* Selenium was version 3.141.0
* geckodriver 0.29.0 (cf6956a5ec8e 2021-01-14 10:31 +0200)
* Firefox 86.0(64-bit)
* hosting OS was Windows 10 (20H2)

* Python 3.7.3 
* Selenium was version 3.141.0
* geckodriver 0.23.0
* Firefox 78.8.0esr
* hosting OS was Linux raspberrypi 5.4.83-v7+ #1379 SMP Mon Dec 14 13:08:57 GMT 2020 armv7l GNU/Linux


* Python 3.8.5
* Selenium was version 3.141.0
* geckodriver 0.29.0
* Firefox 86.0
* Linux Ubuntu 20.04.1
```

## Setup

## Edit tplinkm4.json

```
[
    {
        "log_level": "INFO",
        "ip": "<your_ip_of_the_main_m4r>",
        "password": "<your_password>",
        "browser": "Firefox",
        "browser_display": "no",
        "execute_reboot": "yes",
        "text_reboot": "Reboot",
        "text_reboot_all": "REBOOT ALL",
        "text_model": "M4R",
        "mqtt_use": "yes",
        "mqtt_ip": "<your_mqtt_ip>",
        "mqtt_port": 1883,
        "mqtt_topic": "deco_status"
    }
]
```
| Name          | value allowed        | Remark|
|:---|:---:|:---|
| log_level      | [debug/info/warning/error/critical] | sets the log level|
| ip      | string | the IP of your main M4R device|
| password      | string   | your password to login to the device or same as app |
| browser | [Firefox/Chrome]   | One of the two browser is supported |
| browser_display | [yes/no]   | Yes, will display the browser, in case you want to see what happening, will only work on graphical session |
| execute_reboot | [yes/no]  | "No" will only do a simulation and not click on the final rebbot confirm, most used for testing |
| text_reboot | string  | The label text of the reboot button|
| text_reboot_all | string | The button text of the reboot all button|
| text_model | string | The text of a device in the list; used for waiting|
| mqtt_use | [yes/no]  | Use mqtt messaging?|
| mqtt_ip | string | The mqtt ip adress|
| mqtt_port | int | the mqtt server port; default 1883|
| mqtt_topic | string | The mqtt topic to publish to, mask \\ with double \\\\|


# Install

Here I listed some steps to get this thing going from the start. In case you use different configs or OSs or got already other stuff (versions) installed, I do not mention how to get this working here. This is more "from scratch" instruction.

## Pre-requisite
You need one device that runs constantly (or at that time of reboot). And you do not wan tto use a smart plug to toggle power.

### Windows (10)
* Install obviously python (assuming default settings) 3.7 (newer may also work, not tested)
* install with pip selenium
```
pip install selenium
pip install paho-mqtt
```
* Get geckodriver(.exe) as zip from 
https://github.com/mozilla/geckodriver/releases, extract the geckodriver.exe
and place it in the same folder as the tpLinkM4Reboot.py  


### Linux
#### FreeBSD
(for Python 3.7.9 - otherwise change py37 to the verison used 'python3 --version')
````
* pkg install python3 py37-pip firefox-esr geckodriver
* pip install selenium
* pip install paho-mqtt
````

#### Ubuntu
````
* sudo apt-get update
* sudo apt-get upgrade  
* sudo apt-get install python3 python3-pip firefox-esr firefox-geckodriver
* pip3 install selenium
* pip3 install paho-mqtt
````
#### Raspian / pi 3 or 4
````
* sudo apt-get update
* suod apt-get upgrade
* sudo apt-get install python3 python3-pip firefox-esr firefox-geckodriver
* pip3 install selenium
* pip3 install paho-mqtt
````
On Raspi 2 or earlier it is very hard to find the packages. 
But if you are that familiar with getting selenium on arm61, I guess you won't need this readme also not really, right?:-)

## this package
* Get tpLinkM4Reboot.py and tplinkm4.json from this repository
```
Click on "Code" (green button on top), than select "Download ZIP"
Extract the Content to some writable folder. Eg. ~/tplink 
```
or (for Linux)
```
* mkdir ~/tplink; cd ~/tplink
* wget https://github.com/uptoratlen/tpLinkM4Reboot/archive/main.zip ; unzip -j main.zip
* chmod 775 ~/tplink/*
```

# Usage
## commandline (linux)
````
python3 tpLinkM4Reboot.py
````
## commandline (windows)
````
python tpLinkM4Reboot.py
````
The assumption is only python 3.x is installed. 

## windows - taskscheduler (commandline add)
assumption the script is in **c:\\tplink\\**, otherwise adjust accordingly.
The tpLinkM4Reboot.cmd is used to get the correct working directory and some log output.
````
SCHTASKS /CREATE /SC DAILY /TN "tpLinkM4Reboot (daily)" /TR "cmd /c tpLinkM4Reboot.cmd" /ST 03:00
````
hint: You could change the task later via the taskschd.msc

## linux - cron job
assumption is that the user and home dir is /home/pi/tplink
add command to crontab
````
sudo crontab -e
````
add a line like this
path to python3 may be different and also the user, but you sure will be able to adjust that.
````
0 3 * * * /usr/bin/python3 /home/pi/tplink/tpLinkM4Reboot.py
````
This eg. would execute the script every day at 03:00 in the night.

Hint: https://crontab.guru will help you on creating the right time string for crontab 

If the crontab does not find the selenium (as it runs under a different env) add this also to the crontab
And to be honest that depends on the user, path, os. Maybe there is a better way, but at least for me it worked that way.

````
sudo crontab -e
````
add this before the tpLinkM4Reboot line (yes inside the crontab)
````
PYTHONPATH=/home/pi/.local/lib/python3.7/site-packages
````
This is for python 3.7 and the user pi, on the target system maybe the path is a different one or the user or the path.
Adjust the command based on the sample given.

## logging
The program writes a rolling (10 enumerations) log in the same folder as the .py file withthe name: tpLinkM4Reboot.log  
Sample log (with a "execute_reboot"="no" - so no real reboot is logged)
```
[2021-03-27 22:19:38] - INFO - [root.<module>:59] - Password:*********
[2021-03-27 22:19:38] - INFO - [root.<module>:65] - Browser [Firefox] now open on ip:xxx.xxx.xxx.xxx
[2021-03-27 22:19:41] - INFO - [root.<module>:76] - Click now on login button
[2021-03-27 22:19:50] - INFO - [root.<module>:82] - Logged in successful
[2021-03-27 22:19:50] - INFO - [root.<module>:88] - Wait for all devices to show up in list
[2021-03-27 22:19:58] - INFO - [root.<module>:93] - Ready to Reboot
[2021-03-27 22:20:01] - INFO - [root.<module>:110] - aborting for test - no reboot triggered

```

# Future
* ~~Rolling Logs from within python~~ done since 27. March 2021
* ~~Notification method of success and/or fail (mail?)~~ a MQTT message is implemented
* ....

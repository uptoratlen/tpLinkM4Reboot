# tpLinkM4Reboot

## Overview
What it does. Well lets demonstrate it in a video.
[Demo Video](http://www.kastaban.de/demo_mp4/tpLinkReboot-Demo.mp4 "Demo Video")  
I blurred the video, but if you are familiar withthe webpage, you will see what it does and how it navigates.

The steps the automation does are:
* sign in 
* navigate to the reboot page
* wait for all devices to show up (not sure if needed, but I wait for at least one/all)
* click on reboot
* confirm reboot

## Technologies
The tpLinkM4Reboot obviously was created in Python with Selenium and the geckodriver(firefox) and or chromedriver (Chrome)-
I used to test with firefox but in case oyu prefer chromium, that shoul dbe no big deal (see install)


```
* The job ran successful with webpages at 17th March 2021.
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
        "ip": "<your_ip_of_the_main_m4r>",
        "password": "<your_password>",
        "browser": "Firefox",
        "browser_display": "no",
        "execute_reboot": "no",
        "text_reboot": "Reboot",
        "text_reboot_all": "REBOOT ALL",
        "text_model": "M4R"
    }
]
```
| Name          | value allowed        | Remark|
|:---|:---:|:---|
| ip      | string | the IP of your main M4R device|
| password      | string   | your password to login to the device or same as app |
| browser | [Firefox|Chrome]   | One of the two browser is supported |
| browser_display | [yes|no]   | Yes, will display the browser, in case you want to see what happening, will only work on graphical session |
| execute_reboot | [Yes/No] | "No" will only do a simulation and not click on the final rebbot confirm, most used for testing |
| text_reboot | string  | The label text of the reboot button|
| text_reboot_all | string | The button text of the reboot all button|
| text_model | string | The text of a device in the list; used for waiting|



# Install

Here I listed some steps to get this thing going from the start. In case you use different envs or Os or got already other stuff (versions) installed, I do not mention how to get this working here. This is more "from scratch" instruction.

## Pre-requisite

### Windows (10)
* Install obviously python (assuming default settings) 3.7 (newer may also work, not tested)
* install with pip selenium
```
pip install selenium
```
* Get geckodriver(.exe) as zip from 
https://github.com/mozilla/geckodriver/releases, extract the geckodriver.exe
and place it in the same folder as the tpLinkM4Reboot.py  


### Linux
#### Ubuntu
````
* sudo apt-get update
* sudo apt-get upgrade  
* sudo apt-get install python3 python3-pip firefox-esr firefox-geckodriver
* pip3 install selenium
````
#### Raspian / pi 3 or 4
````
* sudo apt-get update
* suod apt-get upgrade
* sudo apt-get install python3 python3-pip firefox-esr firefox-geckodriver
* pip3 install selenium
````
On Raspi 2 or earlier it is very hard to find the packages. 
But if you are that familiar with getting selenium on arm61, I guess you won't need this readme also not really, right?:-)

## this package
* Get tpLinkM4Reboot.py and tplinkm4.json from this repository
```
Click on "Code" (green button on top), than select "Download ZIP"
Extract the Content to some writeable folder. Eg. ~/tplink 
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
````
0 3 * * * /usr/bin/python3 /home/pi/tplink/tpLinkM4Reboot.py >> /home/pi/tplink/log.log 2>&1
````
This eg. would execute the script every day at 03:00 in th enight.

Hint: https://crontab.guru will help you on creating the right time string for crontab 

If the crontab does not find the selenium (as it runs under a different env) add this also to the crontab
And to be honest that depens on the user, path, os. Maybe there is a better way, but at least fo rme it worked that way.

````
sudo crontab -e
````
add this before the tpLinkM4Reboot line (yes inside the crontab)
````
PYTHONPATH=/home/pi/.local/lib/python3.7/site-packages
````
This is for python 3.7 and the user pi, on the target system maybe the path is a different one or the user or the path.
Adjust the command based on the sample given.

# Future
* Rolling Logs from within python
* Notification method of success and/or fail (mail?)
* ....

from datetime import datetime
import json
import logging
import os
import sys
import paho.mqtt.client as mqtt
from logging.handlers import RotatingFileHandler
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as Options_FF
from selenium.webdriver.chrome.options import Options as Options_Chrome
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def publish_to_mqtt(topic, text):
    if user_data[0]['mqtt_use'].lower() == "yes":
        client.publish(f"{topic}", "{\"text\":\"%s \\r %s\"}" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), text))


LOG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/tpLinkM4Reboot.log'

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=10)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - [%(name)s.%(funcName)s:%(lineno)d] - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)
loglvl_allowed = ['debug', 'info', 'warning', 'error', 'critical']

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('tplinkm4.json', 'r') as file:
    user_data = json.loads(file.read())
mqtt_topic = user_data[0]['mqtt_topic']

log_level = logging.getLevelName('DEBUG')
if user_data[0]['log_level'].lower() in loglvl_allowed:
    log_level = logging.getLevelName(user_data[0]['log_level'].upper())
else:
    logging.debug("Switch back to Debug Level as user used a unexpected value in log level")
logger.setLevel(log_level)

if user_data[0]['mqtt_use'].lower() == "yes":
    client = mqtt.Client()
    client.connect(user_data[0]['mqtt_ip'], user_data[0]['mqtt_port'], 60)

browser_display = user_data[0]['browser_display'].lower()

if user_data[0]['browser'].lower() == "firefox":
    # Firefox
    options = Options_FF()
    options.headless = True
    if browser_display == "yes":
        options.headless = False
    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path='geckodriver')
elif user_data[0]['browser'].lower() == "chrome":
    # Chrome
    chrome_options = Options_Chrome()
    if not browser_display == "yes":
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')
else:
    logging.exception("Browser selected that is not supported [firefox|chrome]")
    exit(9)


logging.info(f"Password:{user_data[0]['password']}")
try:

    url = f"http://{user_data[0]['ip']}"
    wait = WebDriverWait(driver, 10)

    # open browser and login
    logging.info(f"Browser [{user_data[0]['browser']}] now open on ip:{user_data[0]['ip']}")
    driver.get(url)
    # wait for login field
    wait.until(ec.visibility_of_element_located((By.ID, "local-login-pwd")))
    # type in password from json
    #driver.find_element_by_css_selector('input.text-text:nth-child(1)').send_keys(user_data[0]['password'])
    driver.find_element(By.CSS_SELECTOR, 'input.text-text:nth-child(1)').send_keys(user_data[0]['password'])
    # wait for fading overlay to disapear / does not yet fully work
    # wait.until(ec.invisibility_of_element_located((By.XPATH,
    #                                                "//div[@class='center-part']")))
    sleep(2)
    # click on login
    logging.info(f"Click now on login button")
    #driver.find_element_by_link_text("LOG IN").click()
    driver.find_element(By.LINK_TEXT, "LOG IN").click()

    # wait for first page loaded
    wait = WebDriverWait(driver, 60)
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "folder-tree-folder-node-text")))
    logging.info("Logged in successful")

    # navigate to the reboot page
    driver.get(f'{url}/webpages/index.html#reboot')

    # for for the list to be displayed / assumption is that all devices show up at the same time
    logging.info("Wait for all devices to show up in list")
    wait.until(ec.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'content') "
                                                           f"and text()='{user_data[0]['text_model']}']")))

    # prepare reboot
    logging.info("Ready to Reboot")

    #driver.find_element_by_link_text(f"{user_data[0]['text_reboot_all']}").click()
    driver.find_element(By.LINK_TEXT,f"{user_data[0]['text_reboot_all']}").click()

    # wait for the reboot overlay
    wait = WebDriverWait(driver, 10)
    wait.until(ec.visibility_of_element_located((By.XPATH, f"//span[contains(@class, 'text button-text') "
                                                           f"and text()='{user_data[0]['text_reboot']}']")))
    # here something may obscure again
    sleep(2)
    if user_data[0]['execute_reboot'].lower() == "yes":
        # reboot finally
        logging.info("Rebooting...(may take 60s)")
        #driver.find_element_by_xpath(f"//span[contains(@class, 'text button-text') "
        #                             f"and text()='{user_data[0]['text_reboot']}']").click()
        driver.find_element(By.XPATH,(f"//span[contains(@class, 'text button-text') "
                                     f"and text()='{user_data[0]['text_reboot']}']")).click()
        publish_to_mqtt(mqtt_topic, 'Rebooting now')
        sleep(10)
    else:
        logging.info("aborting for test - no reboot triggered")
        publish_to_mqtt(mqtt_topic, 'no reboot triggered')
except Exception:
    publish_to_mqtt(mqtt_topic, 'Something failed - check log')
finally:
    driver.quit()
    client.disconnect()
    exit()

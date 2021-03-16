import json
import logging
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
profile.set_preference("pdfjs.disabled", True)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path='geckodriver')

with open('tplinkm4.json', 'r') as file:
    user_data = json.loads(file.read())

logging.basicConfig(format='%(asctime)s:[%(levelname)-5.5s]  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG, filename='tpLinkM4Reboot.log')

logging.info(f"Password:{user_data[0]['password']}")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
url = f"http://{user_data[0]['ip']}"
wait = WebDriverWait(driver, 10)

# open browser and login
logging.info(f"Browser now open on ip:{user_data[0]['ip']}")
driver.get(url)
# wait for login field
wait.until(ec.visibility_of_element_located((By.ID, "local-login-pwd")))
# type in password from json
driver.find_element_by_css_selector('input.text-text:nth-child(1)').send_keys(user_data[0]['password'])
# wait for fading overlay to disapear / does not yet fully work
# wait.until(ec.invisibility_of_element_located((By.XPATH,
#                                                "//div[@class='center-part']")))
sleep(2)
# click on login
logging.info(f"Click now on login button")
driver.find_element_by_link_text("LOG IN").click()

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

driver.find_element_by_link_text(f"{user_data[0]['text_reboot_all']}").click()

# wait for the reboot overlay
wait = WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((By.XPATH, f"//span[contains(@class, 'text button-text') "
                                                       f"and text()='{user_data[0]['text_reboot']}']")))
# here something may obscure again
sleep(2)
logging.info("aborting for test - no reboot triggered")
exit(99)
# reboot finally
logging.info("Rebooting...(may take 60s)")
driver.find_element_by_xpath(f"//span[contains(@class, 'text button-text') "
                             f"and text()='{user_data[0]['text_reboot']}']").click()

sleep(10)
driver.quit()
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # enter key
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

path = ".\chromedriver.exe"
driver = webdriver.Chrome(path)
#service = Service('./chromedriver')
#service.start()

#driver = webdriver.Remote(service.service_url)
driver.get("https://utils.bim.emsd.gov.hk/aimp/index")
driver.maximize_window()

user = driver.find_element_by_id("userName")
user.send_keys("Forida")
pw = driver.find_element_by_id("password")
pw.send_keys("123456")
pw.send_keys(Keys.RETURN)
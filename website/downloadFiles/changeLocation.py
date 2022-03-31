import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # enter key
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from .waiting import Wait


def changeLocation(driver):
# ################################################################################################################
# # Choose the Project
    content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "root")))
##########################################################################################################
#Forida(HKBCF)
    Forida_HKBCF=True
    while(Forida_HKBCF):
        try:
            button1 = Wait(20, '//button[@class="ant-btn ant-dropdown-trigger"]',driver)
            button1.click()
##########################################################################################################
    #Change Functional Location
            button2 = Wait(20, '//li[@class="ant-dropdown-menu-item"]',driver)
            button2.click()
            Forida_HKBCF=False
        except selenium.common.exceptions.TimeoutException:
            pass
        except selenium.common.exceptions.ElementClickInterceptedException:
            pass
    # ##########################################################################################################
    # #wait for user change the project
    button3 = Wait(20, '//div[@class="ant-select-selection-selected-value"]',driver)
    please_select = driver.find_element_by_xpath("//div[@class='ant-select-selection-selected-value']").text
    button3.click()
    Change = False
    while (not Change):
        location = driver.find_element_by_xpath("//div[@class='ant-select-selection-selected-value']").text
        if (location != please_select):
            print(f"location : {location} \n")
            Change = True

    confirm = driver.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary' and span='Confirm']").click()
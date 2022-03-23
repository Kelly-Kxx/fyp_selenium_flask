import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # enter key
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

def findrow(driver):
    row= driver.find_elements_by_xpath(
        "//tr[@class='ant-table-row ant-table-row-level-0']//td[@class]")
    id=row[0].text
    status=row[2].text
    return id,status

def click_to_export(driver):
    driver.find_element_by_xpath(
    "//*[@id='root']/div/section/section/main/div[1]/div[1]/div/div[9]/button").click()

def checkOperationID(driver):
    old_id = findrow(driver)[0]
    click_to_export(driver)
    new_id = findrow(driver)[0]
    new_status = findrow(driver)[1]
    while (old_id == new_id):
        new_id = findrow(driver)[0]
        new_status = findrow(driver)[1]
    return 


def download(driver): 
###############################################################################################################
#Check for the id in Operation ID
    old_id = findrow(driver)[0]
    click_to_export(driver)
    new_id = findrow(driver)[0]
    new_status = findrow(driver)[1]
    while (old_id == new_id):
        new_id = findrow(driver)[0]
        new_status = findrow(driver)[1]
###############################################################################################################
    #count the time for the pending
    starttime= time.time()
    counter=1
    while (old_id != new_id and new_status == "Pending" and counter<=2):
        elapsedtime=time.time()-starttime
        if(elapsedtime<60): #less than 5s
            new_id = findrow(driver)[0]
            new_status = findrow(driver)[1]
        else:
            click_to_export(driver)
            counter+=1
            starttime=time.time()
    if(counter==3): #do it 3 times
        return (False,None)
    ###############################################################################################################
    #click the download button
    #Need unzip files
    Check = True
    while (Check and new_status == "Complete"):
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
            "//*[@id='root']/div/section/section/main/div[1]/div[3]/div[1]/div/div/div/div/div/div/table/tbody/tr[1]/td[12]/span/a")))
            
            down=driver.find_element_by_xpath(
            "//*[@id='root']/div/section/section/main/div[1]/div[3]/div[1]/div/div/div/div/div/div/table/tbody/tr[1]/td[12]/span/a").click()
            Check = False
        except selenium.common.exceptions.ElementNotInteractableException:
            Check = True
        return (True,down)
    return(False,None)
#from pandas.core.frame import DataFrame
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # enter key
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from download_CCS import download_CCS_one_file
from waiting import Wait, InputField_Alltable
from download import findrow, click_to_export, download_Condition, column_export
from changeLocation import changeLocation
#from dir import sort_dir

path = r"./chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)
def main():
    driver.get("https://utils.bim.emsd.gov.hk/aimp/index")
    driver.maximize_window()

    user = driver.find_element_by_id("userName")
    user.send_keys("Forida")
    pw = driver.find_element_by_id("password")
    pw.send_keys("123456")
    pw.send_keys(Keys.RETURN)
    changeLocation(driver)
##########################################################################################################
# click the export
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-layout-sider-children']")))
    column_export(driver)
  
    output_files = InputField_Alltable(driver,0)[0].find_elements_by_tag_name("li")
    output_files[1].click()
    driver.implicitly_wait(3)
    Systems = InputField_Alltable(driver,1)[1].find_elements_by_tag_name("li")
    for sys in range(3): # (len(Systems))
        Systems[sys].click()
        driver.implicitly_wait(3)
        Devices = InputField_Alltable(driver,2)[2].find_elements_by_tag_name("li")
        for device in range(len(Devices)):  # (len(Devices))
            download_CCS_one_file(driver, 1, sys, device)
        Systems = InputField_Alltable(driver,1)[1].find_elements_by_tag_name("li")
   


main()
driver.quit()
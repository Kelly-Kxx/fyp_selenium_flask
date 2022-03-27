from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
def Wait(waiting_time, xpath, driver):
    return WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

def InputField_Alltable(driver, inputfield_index): #Find Systems, Devices
    #can click the inputfield and output the outputfiles
    can_click = True
    while (can_click):
        try:
            InputField = driver.find_elements_by_xpath("//div[@class='ant-select-selection-selected-value']")
            Wait(20,"//div[@class='ant-select-selection-selected-value']", driver)
            InputField[inputfield_index].click()
            can_click = False
            All_table = driver.find_elements_by_xpath(
                "//ul[@class='ant-select-dropdown-menu  ant-select-dropdown-menu-root ant-select-dropdown-menu-vertical']")
                
        except selenium.common.exceptions.TimeoutException:
            pass
        except selenium.common.exceptions.ElementClickInterceptedException:
            pass
    return All_table
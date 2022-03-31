from .waiting import Wait, InputField_Alltable
from .download import findrow, click_to_export, download_Condition
from selenium.webdriver.common.action_chains import ActionChains
import selenium

def click_system(driver,Systems, sys):
    sys_bool = True
    while (sys_bool):
        try:
            Systems[sys].click()
            sys_bool=False
            return Systems[sys].get_attribute('innerHTML')
        except selenium.common.exceptions.ElementNotInteractableException:
            pass

def click_device(driver,Devices, dev):
    sys_bool = True
    while (sys_bool):
        try:
            # Devices[dev].click()
            sys_bool=False
            ActionChains(driver).move_to_element(Devices[dev]).click(Devices[dev]).perform()
            return Devices[dev].get_attribute('innerHTML')
        except selenium.common.exceptions.ElementNotInteractableException:
            pass


def download_CCS_one_file(driver, filetype,sys,device):  #filetype always be 1
    driver.implicitly_wait(3)
    Systems = InputField_Alltable(driver,1)[1].find_elements_by_tag_name("li")
    current_sys_name = click_system(driver,Systems, sys)
################################################################################################################
    Devices = InputField_Alltable(driver,2)[2].find_elements_by_tag_name("li")
    driver.implicitly_wait(20)
    current_device_name = click_device(driver,Devices,device)
    print(f"device {device} , current_device_name: {current_device_name} ")
    checking = download_Condition(driver)  # check whether it can download or not. If not, put in Cannot_download list
################################################################################################################
# need click the inputfield, pop out the list
    driver.implicitly_wait(20)
    if (checking[0] == False):
  
        print("Fail to Download [filetype,sys,device] ",["CCS", current_sys_name, current_device_name])
        #return(False,[filetype,sys,device])
        return (False, ["CCS", current_sys_name, current_device_name])
    else:
        print("Downloaded", ["CCS", current_sys_name, current_device_name])
        DOWNLOADS=r"C:/Users/Kei Ka Shun/Downloads" 
        #sort_dir(DOWNLOADS,location, current_sys_name, current_device_name)
        return (True,checking[1])


# def download_CCS(filetype,sys,device):  #filetype always be 1
#     driver.implicitly_wait(3)
#     Systems = InputField_Alltable(driver,1)[1].find_elements_by_tag_name("li")
#     sys_bool = True
#     while (sys_bool):
#         try:
#             Systems[sys].click()
#             sys_bool=False
#         except selenium.common.exceptions.ElementNotInteractableException:
#             pass

# ################################################################################################################
#     Devices = InputField_Alltable(driver,2)[2].find_elements_by_tag_name("li")
#     driver.implicitly_wait(20)
#     can_click=True
#     current_sys_name = Systems[sys].get_attribute('innerHTML')
#     current_device_name = Devices[device].get_attribute('innerHTML')
#     print(f"device {device} , current_device_name: {current_device_name} ")
#     while (can_click):
#         try:
#             Devices[device].click()
#             can_click=False
#         except selenium.common.exceptions.ElementClickInterceptedException:
#             pass

#     checking = download_Condition(driver)  # check whether it can download or not. If not, put in Cannot_download list
# ################################################################################################################
# # need click the inputfield, pop out the list
#     driver.implicitly_wait(20)
#     current_sys_name = Systems[sys].get_attribute('innerHTML')
#     current_device_name = Devices[device].get_attribute('innerHTML')
    
#     if (checking[0] == False):
  
#         print("Fail to Download [filetype,sys,device] ",["CCS", current_sys_name, current_device_name])
#         #return(False,[filetype,sys,device])
#         return (False, ["CCS", current_sys_name, current_device_name])
#     else:
#         print("Downloaded", ["CCS", current_sys_name, current_device_name])
#         DOWNLOADS=r"C:/Users/Kei Ka Shun/Downloads" 
#         #sort_dir(DOWNLOADS,location, current_sys_name, current_device_name)
#         return (True,checking[1])
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

from waiting import Wait
from download import findrow, click_to_export, download_Condition
#from dir import sort_dir

path = "./chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://utils.bim.emsd.gov.hk/aimp/index")
driver.maximize_window()

user = driver.find_element_by_id("userName")
user.send_keys("Forida")
pw = driver.find_element_by_id("password")
pw.send_keys("123456")
pw.send_keys(Keys.RETURN)







def InputField_Alltable(inputfield_index): #Find Systems, Devices
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






def download_CCS(filetype,sys,device):  #filetype always be 1
    driver.implicitly_wait(3)
    Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")
    sys_bool = True
    while (sys_bool):
        try:
            Systems[sys].click()
            sys_bool=False
        except selenium.common.exceptions.ElementNotInteractableException:
            pass

################################################################################################################
    Devices = InputField_Alltable(2)[2].find_elements_by_tag_name("li")
    driver.implicitly_wait(20)
    can_click=True
    current_sys_name = Systems[sys].get_attribute('innerHTML')
    current_device_name = Devices[device].get_attribute('innerHTML')
    print(f"device {device} , current_device_name: {current_device_name} ")
    while (can_click):
        try:
            Devices[device].click()
            can_click=False
        except selenium.common.exceptions.ElementClickInterceptedException:
            pass

    checking = download_Condition(driver)  # check whether it can download or not. If not, put in Cannot_download list
################################################################################################################
# need click the inputfield, pop out the list
    driver.implicitly_wait(20)
    current_sys_name = Systems[sys].get_attribute('innerHTML')
    current_device_name = Devices[device].get_attribute('innerHTML')
    
    if (checking[0] == False):
  
        print("Fail to Download [filetype,sys,device] ",["CCS", current_sys_name, current_device_name])
        #return(False,[filetype,sys,device])
        return (False, ["CCS", current_sys_name, current_device_name])
    else:
        print("Downloaded", ["CCS", current_sys_name, current_device_name])
        DOWNLOADS=r"C:/Users/Kei Ka Shun/Downloads" 
        #sort_dir(DOWNLOADS,location, current_sys_name, current_device_name)
        return (True,checking[1])

# ################################################################################################################
# # Choose the Project
content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "root")))
# ##########################################################################################################
# #Forida(HKBCF)
Forida_HKBCF=True
while(Forida_HKBCF):
    try:
        button1 = Wait(20, '//button[@class="ant-btn ant-dropdown-trigger"]',driver)
        button1.click()
# ##########################################################################################################
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
##########################################################################################################
# click the export
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-layout-sider-children']")))
waiting=True
while(waiting):
    try:
        export = driver.find_elements_by_xpath("//li[@role='menuitem']")
        export[4].click()
        waiting=False
    except selenium.common.exceptions.StaleElementReferenceException:
        pass
# driver.get('chrome://settings/')
# driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.5);')
# driver.back()
# ##############################################################################
# #real part

filetype=1
Cannot_download_index=[]
list_or_download=[]
output_files = InputField_Alltable(0)[0].find_elements_by_tag_name("li")

while(filetype<len(output_files)):
    output_files[filetype].click()
    if(filetype==1):
        driver.implicitly_wait(3)
        Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")
        for sys in range(3): # (len(Systems))
    
            Systems[sys].click()
            
            driver.implicitly_wait(3)
            Devices = InputField_Alltable(2)[2].find_elements_by_tag_name("li")
          
            for device in range(len(Devices)):  # (len(Devices))
                list_or_download = download_CCS(filetype, sys, device)
            
            Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")
    # else:
    #     if(filetype!=5):
    #         click_to_export()
    #         checking=download()
    #         print(filetype)
    #         if(checking[0]==False):
    #             Cannot_download_index.append([filetype])
    #             driver.implicitly_wait(20)
# ##############################################################################################################
    output_files = InputField_Alltable(0)[0].find_elements_by_tag_name("li")
    driver.implicitly_wait(10)
    filetype+=1
# # ###############################################################################################################
# # #redownload
def outputfiletype(filetype):
    can_click = True
    while (can_click):
        try:
            output_files = InputField_Alltable(0)[0].find_elements_by_tag_name("li")
            driver.implicitly_wait(3)
            output_files[filetype].click()
            can_click=False
        except selenium.common.exceptions.TimeoutException:
            pass
        except selenium.common.exceptions.ElementClickInterceptedException:
            pass
    return output_files

###############################################################################################################
#redownload
index=0
print("redownload")
while(index<len(Cannot_download_index)):
    val=Cannot_download_index[index]#[1,0,1],[2]
    print("val",val)
    filetype=val[0]
    output_files = outputfiletype(filetype)
    if(len(val)==3):
      
        check_download=download_CCS(1, val[1], val[2])
        if(check_download[0]==False):
            print("check_download[1]", check_download[1])
            index+=1
        else:
            Cannot_download_index.remove(index)
    elif(len(val)==1): #if length val ==1
        if(filetype!=5):
            click_to_export()
            checking=download(driver)
            if(checking[0]==False):
                print(val[0])
                driver.implicitly_wait(20)
                index+=1
            else:
                Cannot_download_index.remove(index)
print(Cannot_download_index)
# ##############################################################################################################

# #
# #
# #
# #
driver.quit()
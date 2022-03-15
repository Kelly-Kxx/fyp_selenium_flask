from genericpath import isfile
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # enter key
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
from zipfile import ZipFile, ZipInfo
import os
from openpyxl.reader.excel import ExcelReader
import openpyxl
##########################################################################################
#create Zipfile EMSD folder
isdir=os.path.isdir(r"C:\Users\Kei Ka Shun\Desktop\Zipfile")
if(not isdir):
    os.mkdir(r"C:\Users\Kei Ka Shun\Desktop\Zipfile")

isdir=os.path.isdir(r"C:\Users\Kei Ka Shun\Desktop\EMSD")
if(not isdir):
    os.mkdir(r"C:\Users\Kei Ka Shun\Desktop\EMSD")
##########################################################################################
#move from download to Zipfile

ori_path=r"Downloads" #Downloads
ori_files= os.listdir(ori_path)
zip_path=r"C:/Users/Kei Ka Shun/Desktop/Zipfile"

for files in ori_files:
    name=os.path.splitext(files) #('ziptodownload_CSS_HKBCF_GE12101_20210718_120720_forida', '.zip')
    if(name[1]==".zip"):
        if("ziptodownload" in name[0]):
            filepath=os.path.join(ori_path,files)
            shutil.move(filepath,zip_path)

##########################################################################################
#Unzip in vir-env then move unzip file to EMSD file 
EMSD=r"C:\Users\Kei Ka Shun\Desktop\EMSD"
current_working_dir= os.getcwd()
for root,directory,file in os.walk(zip_path):
 for filename in file:
     zip_file_path=os.path.join(root,filename)
     with ZipFile(zip_file_path,'r') as zip:
         checkfile=os.path.join(EMSD,zip.namelist()[0])
         if(os.path.isfile(checkfile)==False):
             zip.extractall()
             unzip_filepath=os.path.join(current_working_dir,zip.namelist()[0])
             shutil.move(unzip_filepath,EMSD)

##########################################################################################
#loop in excel
for excel_file in os.listdir(EMSD):
    excel_path=os.path.join(EMSD,excel_file)
    workbook=openpyxl.load_workbook(excel_path)
    worksheet=workbook.active

    print("hi!!!!!!!!!!!!!!!! \n")
    print(worksheet.title)
    
    max_i=0
    for cell in worksheet['D']:
        if cell.row >=20:
            if cell.value is not None:
                max_i=int(cell.row)
    i=20
    row_list=[]
    table_list=[]

    while i<=max_i: 
        for cell in worksheet[i]:
            if cell.value is not None:            
                row_list.append(cell.value)
        table_list.append(row_list.copy())
        row_list.clear()
        i+=1

    for i in table_list:
        print(i,'\n')
        print(i[0],'\n')
    print(max_i)

##########################################################################################################






##########################################################################################################
# path = "chromedriver.exe"
# driver = webdriver.Chrome(path)
# driver.get("https://utils.bim.emsd.gov.hk/aimp/index")
# driver.maximize_window()
# ##########################################################################################################
# user = driver.find_element_by_id("userName")
# user.send_keys("Forida")
# pw = driver.find_element_by_id("password")
# pw.send_keys("123456")
# pw.send_keys(Keys.RETURN)
# ##########################################################################################################
# def Wait(waiting_time, xpath):
#     return WebDriverWait(driver, waiting_time).until(
#         EC.element_to_be_clickable((By.XPATH, xpath))
#     )
# def click_to_export():
#     driver.find_element_by_xpath(
#         "//*[@id='root']/div/section/section/main/div[1]/div[1]/div/div[6]/button").click()
# def findrow():
#     row= driver.find_elements_by_xpath(
#         "//tr[@class='ant-table-row ant-table-row-level-0']//td[@class]")
#     id=row[0].text
#     status=row[2].text
#     return id,status
# def download(): #not yet done
#     old_id = findrow()[0]
#     click_to_export()
#     new_id = findrow()[0]
#     new_status = findrow()[1]
#     while (old_id == new_id):
#         new_id = findrow()[0]
#         new_status = findrow()[1]
# ###############################################################################################################
#     #count the time for the pending
#     starttime= time.time()
#     counter=1
#     while (old_id != new_id and new_status == "Pending" and counter<=2):
#         elapsedtime=time.time()-starttime
#         if(elapsedtime<5): #less than 5s
#             new_id = findrow()[0]
#             new_status = findrow()[1]
#         else:
#             click_to_export()
#             counter+=1
#             starttime=time.time()
#     if(counter==3):
#         return (False,None)
#     ###############################################################################################################
#     #click the download button
#     #Need unzip files
#     Check = True
#     while (Check and new_status == "Complete"):
#         try:
#             WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
#             "//*[@id='root']/div/section/section/main/div[1]/div[3]/div[1]/div/div/div/div/div/div/table/tbody/tr[1]/td[11]/span/a")))
#             down=driver.find_element_by_xpath(
#             "//*[@id='root']/div/section/section/main/div[1]/div[3]/div[1]/div/div/div/div/div/div/table/tbody/tr[1]/td[11]/span/a").click()
#             Check = False
#         except selenium.common.exceptions.ElementNotInteractableException:
#             Check = True
#         return (True,down)

# def InputField_Alltable(inputfield_index): #Find Systems, Devices
#     #can click the inputfield and output the outputfiles
#     can_click = True
#     while (can_click):
#         try:
#             InputField = driver.find_elements_by_xpath("//div[@class='ant-select-selection-selected-value']")
#             Wait(20,"//div[@class='ant-select-selection-selected-value']")
#             InputField[inputfield_index].click()
#             can_click = False
#             All_table = driver.find_elements_by_xpath(
#                 "//ul[@class='ant-select-dropdown-menu  ant-select-dropdown-menu-root ant-select-dropdown-menu-vertical']")
#         except selenium.common.exceptions.TimeoutException:
#             pass
#         except selenium.common.exceptions.ElementClickInterceptedException:
#             pass
#     return All_table




# def download_CCS(filetype,sys,device):  #filetype always be 1
#     driver.implicitly_wait(3)
#     Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")
#     Systems[sys].click()
#     driver.implicitly_wait(3)
# ################################################################################################################
#     Devices = InputField_Alltable(2)[2].find_elements_by_tag_name("li")
#     driver.implicitly_wait(20)
#     Devices[device].click()
#     checking = download()  # check whether it can download or not. If not, put in Cannot_download list
# ################################################################################################################
# # need click the inputfield, pop out the list
#     driver.implicitly_wait(20)
#     if (checking[0] == False):
#         print("filetype,sys,device",[filetype,sys,device])
#         return(False,[filetype,sys,device])
#     else:
#         print("checking[1]=",checking[1])
#         return (True,checking[1])

# ################################################################################################################
# # Choose the Project
# content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "root")))
# ##########################################################################################################
# #Forida(HKBCF)
# Forida_HKBCF=True
# while(Forida_HKBCF):
#     try:
#         button1 = Wait(20, '//button[@class="ant-btn ant-dropdown-trigger"]')
#         button1.click()
# ##########################################################################################################
# #Change Functional Location
#         button2 = Wait(20, '//li[@class="ant-dropdown-menu-item"]')
#         button2.click()
#         Forida_HKBCF=False
#     except selenium.common.exceptions.TimeoutException:
#         pass
#     except selenium.common.exceptions.ElementClickInterceptedException:
#         pass
# ##########################################################################################################
# #wait for user change the project
# button3 = Wait(20, '//div[@class="ant-select-selection-selected-value"]')
# old_value = driver.find_element_by_xpath("//div[@class='ant-select-selection-selected-value']").text
# button3.click()
# Change = False
# while (not Change):
#     new_value = driver.find_element_by_xpath("//div[@class='ant-select-selection-selected-value']").text
#     if (new_value != old_value):
#         Change = True

# confirm = driver.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary' and span='Confirm']").click()
# ##########################################################################################################
# # click the export
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-layout-sider-children']")))
# waiting=True
# while(waiting):
#     try:
#         export = driver.find_elements_by_xpath("//li[@role='menuitem']")
#         export[4].click()
#         waiting=False
#     except selenium.common.exceptions.StaleElementReferenceException:
#         pass
# ###############################################################################################################
# # Export page

# ################debug##############################################################
# filetype=1
# Cannot_download_index=[]
# list_or_download=[]
# output_files = InputField_Alltable(0)[0].find_elements_by_tag_name("li")
# output_files[filetype].click()
# if(filetype==1):
#     driver.implicitly_wait(3)
#     Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")
#     for sys in range(2):
#         Systems[sys].click()
#         driver.implicitly_wait(3)
#         Devices = InputField_Alltable(2)[2].find_elements_by_tag_name("li")
#         for device in range(2): #(len(Devices))
#             list_or_download=download_CCS(filetype,sys,device)
#             print(list_or_download[0],list_or_download[1])
#             if(list_or_download[0]==False):
#                 Cannot_download_index.append(list_or_download[1])
#         Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")

# ##############################################################################
# #real part

# # filetype=1
# # Cannot_download_index=[]
# # list_or_download=[]
# # output_files = InputField_Alltable(0)[0].find_elements_by_tag_name("li")
# # while(filetype<len(output_files)):
# #     output_files[filetype].click()
# #     if(filetype==1):
# #         driver.implicitly_wait(3)
# #         Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")
# #         for sys in range(2):
# #             Systems[sys].click()
# #             driver.implicitly_wait(3)
# #             Devices = InputField_Alltable(2)[2].find_elements_by_tag_name("li")
# #             for device in range(2):  # (len(Devices))
# #                 list_or_download = download_CCS(filetype, sys, device)
# #                 if (list_or_download[0] == False):
# #                     Cannot_download_index.append(list_or_download[1])
# #             Systems = InputField_Alltable(1)[1].find_elements_by_tag_name("li")
# #     else:
# #         if(filetype!=5):
# #             click_to_export()
# #             checking=download()
# #             print(filetype)
# #             if(checking[0]==False):
# #                 Cannot_download_index.append([filetype])
# #                 driver.implicitly_wait(20)
# # ##############################################################################################################
# #     output_files = InputField_Alltable(0)[0].find_elements_by_tag_name("li")
# #     driver.implicitly_wait(10)
# #     filetype+=1
# # ###############################################################################################################
# # #redownload
# def outputfiletype(filetype):
#     can_click = True
#     while (can_click):
#         try:
#             output_files = InputField_Alltable(0)[0].find_elements_by_tag_name("li")
#             driver.implicitly_wait(3)
#             output_files[filetype].click()
#             can_click=False
#         except selenium.common.exceptions.TimeoutException:
#             pass
#         except selenium.common.exceptions.ElementClickInterceptedException:
#             pass
#     return output_files

# index=0
# print("redownload")
# while(index<len(Cannot_download_index)):
#     val=Cannot_download_index[index]#[1,0,1],[2]
#     print(val)
#     filetype=val[0]
#     output_files = outputfiletype(filetype)
#     if(len(val)==3):
#         print(val[1],val[2])
#         check_download=download_CCS(1, val[1], val[2])
#         if(check_download[0]==False):
#             print(check_download[1])
#             index+=1
#         else:
#             Cannot_download_index.remove(index)
#     elif(len(val)==1): #if length val ==1
#         if(filetype!=5):
#             click_to_export()
#             checking=download()
#             if(checking[0]==False):
#                 print(val[0])
#                 driver.implicitly_wait(20)
#                 index+=1
#             else:
#                 Cannot_download_index.remove(index)
# print(Cannot_download_index)
# ##############################################################################################################

# #
# #
# #
# #
# # driver.quit()
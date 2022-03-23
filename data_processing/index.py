
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # enter key
import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
from zipfile import ZipFile, ZipInfo
import os
from openpyxl.reader.excel import ExcelReader
import openpyxl
import json
from dest_files import create_folders, move_files , unzip_files , create_database_file
from db_model import database_model, create_connection, create_table,insert_one_row_data
##########################################################################################
#create Zipfile EMSD folder

EMSD=r"C:/Users/Kei Ka Shun/Desktop/EMSD"
ZIP = r"C:/Users/Kei Ka Shun/Desktop/Zipfile"
DOWNLOADS=r"C:/Users/Kei Ka Shun/Downloads" 

create_folders(ZIP, EMSD)
##########################################################################################
#move from download to Zipfile
move_files(DOWNLOADS, ZIP)
##########################################################################################
#Unzip in vir-env then move unzip file to EMSD file 
unzip_files(ZIP,EMSD)
##########################################################################################
#loop in excel

test = 0
for excel_file in os.listdir(EMSD):
    if(test)>2:
        break
    excel_path=os.path.join(EMSD,excel_file)
    workbook=openpyxl.load_workbook(excel_path)
    worksheet=workbook.active
    #print("Worksheet title",worksheet.title)
    max_i=0
    for cell in worksheet['D']:
        if cell.row >=20:
            if cell.value is not None:
                max_i=int(cell.row)
    i=20
    attr_index = 14
    k = 0
    row_list=[]
    table_list=[]
    attr_list = []
    done = False 
    while i<=max_i: 
        for cell in worksheet[i]:
            if(k>=3):         
                row_list.append(cell.value)
                
                if(not done): # add attr by monnitoring the first row
                    attr_list.append(worksheet[attr_index][k].value)
            k+=1
        done = True
        table_list.append(row_list.copy())
        row_list.clear()
        i+=1
        k=0

##########################################################################################
# Create loc_sys.db
    DB_DEST = r"C:/Users/Kei Ka Shun/Desktop/project-env/FYP-main/website/database"
    loc_sys = excel_file.split('.')[0] #CSS_HKBCF-001_BR1102_20220315_054759_forida
    loc_sys = loc_sys.replace('-','_') #CSS_HKBCF_001_BR1102_20220315_054759_forida
    print(worksheet.title)
    for i in range(len(attr_list)):
        attr_list[i] = re.sub(r'(\(.*|\n*\)|(\.))', '',attr_list[i])  
        attr_list[i] = re.sub(r'-', '_',attr_list[i])
        attr_list[i] = re.sub(r'/', '_',attr_list[i])
        attr_list[i] = re.sub(r' ', '_',attr_list[i])  
        attr_list[i] = re.sub(r'\n', '_',attr_list[i])  
          

    db_file = create_database_file(DB_DEST,loc_sys)
    table_name = loc_sys.split('_')[1] + '_' + loc_sys.split('_')[2] + '_'+ loc_sys.split('_')[3]+'_'+ worksheet.title.split(' ')[0]

    statement = "Equipment_No text PRIMARY KEY,"
    for attr in attr_list[1:]:
        statement += f"{attr} text,"
    
    
    insert_statement = "Equipment_No,"
    for attr in attr_list[1:]:
        insert_statement += f"{attr},"

    
    conn = create_connection(db_file)
    if conn is not None:
        create_table(conn,table_name, statement) # create table
        print(len(table_list))
        for index in range(len(table_list)):
            table_list[index] = str(table_list[index])
            table_list[index] = table_list[index].replace("[",'')
            table_list[index] = table_list[index].replace("]",'')
            table_list[index] = re.sub(r'None', 'NULL',table_list[index])  
            print(table_list[index], '\n')
            insert_one_row_data(conn,table_name,insert_statement,table_list[index]) #insert data insert_query = f"""INSERT INTO {table_name} ({attr}) VALUES({data}); """
    else:
        print("Error! cannot create the database connection.")
    test+=1
    #     if conn:
    #         conn.close()
    #         print("The SQLite connection is closed")







from textwrap import indent
from flask import jsonify
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
from .db_requirement import attr_requirement, item_requirement, table_name_initialization
from .dest_files import create_folders, move_files , unzip_files , create_database_file, rename, getLatestFileTime
from .db_model import  create_connection, create_table,insert_one_row_data, get_data
from .excel_data import proces_excel_data, getLatestTime
from .db_requirement import location_requirement , attr_requirement, table_name_initialization, item_requirement

##########################################################################################
#create Zipfile EMSD folder

EMSD=r"C:/Users/Kei Ka Shun/Desktop/EMSD"
ZIP = r"C:/Users/Kei Ka Shun/Desktop/Zipfile"
DOWNLOADS=r"C:/Users/Kei Ka Shun/Downloads" 
DB_DEST = r"C:/Users/Kei Ka Shun/Desktop/project-env/FYP-main/website/database"

def database_initialization():
    create_folders(ZIP, EMSD)
    ##########################################################################################
    #move from download to Zipfile
    move_files(DOWNLOADS, ZIP)
    ##########################################################################################
    #Unzip in vir-env then move unzip file to EMSD file 
    unzip_files(ZIP,EMSD)
    ##########################################################################################
    #loop in excel
    getLatestFileTime(EMSD,ZIP)
    latest_timestamp = ""
    init_bool = True
    change_log = []
    for excel_file in os.listdir(EMSD):
        if(init_bool):
            latest_timestamp = getLatestTime(excel_file)
            init_bool = False
        else:
            curr_timestamp =  getLatestTime(excel_file)
            if(curr_timestamp > latest_timestamp):
                latest_timestamp = curr_timestamp
        [asset_code, attr_list, table_list] = proces_excel_data(EMSD,excel_file)
        print("excel_file", excel_file)
    ##########################################################################################
    # Create loc_sys.db 
        loc = location_requirement(excel_file)
        asset_code = asset_code.split("-")[:-1]
        attr_list = attr_requirement(attr_list)   
        table_name = table_name_initialization(loc,asset_code)
    ##########################################################################################
    # init db
        db_file= DB_DEST +'/' +loc + ".db"
        
        # print("location", loc)
        if(not os.path.isfile(os.path.join(DB_DEST,loc + ".db"))):
            db_file = create_database_file(DB_DEST,loc)
        conn = create_connection(db_file)
        cursor = conn.cursor()
        if conn is not None:    
            create_table(conn,table_name, attr_list) # create table
            conn.commit()
            print(f"database : {loc}, table name : {table_name} ")   
            # get_data(conn,cursor,table_name)
            for index in range(len(table_list)):
                str_table_item = table_list[index]
                str_table_item = item_requirement(str_table_item)
               
                insert_one_row_data(conn,table_name,attr_list,str_table_item,table_list[index],change_log) #insert data insert_query = f"""INSERT INTO {table_name} ({attr}) VALUES({data}); """
                conn.commit()
                
            # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            # print(cursor.fetchall())
        else:
            print("Error! cannot create the database connection.")

    if conn:
        
        # print(change_log)
        json_string = json.dumps(change_log)

      
        with open('change_log.json', 'w') as outfile:
            json.dump(json.loads(json_string),outfile,indent=4)
        
        conn.close()
        print("The SQLite connection is closed")
        return latest_timestamp

# print("lastest timestamp:", database_initialization())








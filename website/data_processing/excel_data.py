

import os
import openpyxl
from openpyxl.reader.excel import ExcelReader
from datetime import datetime , date, time

def proces_excel_data(EMSD,excel_file):
    asset_code = ""
    excel_path=os.path.join(EMSD,excel_file)
    workbook=openpyxl.load_workbook(excel_path)
    worksheet=workbook.active
    
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
                    asset_code = cell.value
            k+=1
        done = True
        table_list.append(row_list.copy())
        row_list.clear()
        i+=1
        k=0
    return [asset_code,attr_list,table_list]

def getLatestTime(excel_file):
    curr_date = excel_file.split('_')[3]
    curr_date = date(int(curr_date[:4]),int(curr_date[4:6]),int(curr_date[6:]))
    curr_time = excel_file.split('_')[4]
    curr_time = time(int(curr_time[:2]),int(curr_time[2:4]),int(curr_time[4:]))
    curr_datetime = datetime.combine(curr_date,curr_time)
    return curr_datetime
    

from msilib.schema import tables
import os
import openpyxl
from openpyxl.reader.excel import ExcelReader

def proces_excel_data(EMSD,excel_file):
    asset_code = ""
    excel_path=os.path.join(EMSD,excel_file)
    workbook=openpyxl.load_workbook(excel_path)
    worksheet=workbook.active
    print("Worksheet title",worksheet.title)
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
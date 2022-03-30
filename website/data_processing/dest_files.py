import os
import shutil
from zipfile import ZipFile
import sqlite3
from sqlite3 import Error
from pathlib import Path
#from downloadFiles.dir import sort_dir
import os
from datetime import datetime

from pathlib import Path


##########################################################################################
#create Zipfile EMSD folder
def create_folders(zip_files_path, unzipped_path):
    isdir=os.path.isdir(zip_files_path)
    if(not isdir):
        os.mkdir(zip_files_path)

    isdir=os.path.isdir(unzipped_path)
    if(not isdir):
        os.mkdir(unzipped_path)


def move_files(DOWNLOADS, ZIP):
    ori_files= os.listdir(DOWNLOADS)
    for files in ori_files:
        name=os.path.splitext(files) #('ziptodownload_CSS_HKBCF_GE12101_20210718_120720_forida', '.zip')
    
        if(name[1]==".zip"):
            if("forida" in name[0]):
                filepath=os.path.join(DOWNLOADS,files)
                destpath=os.path.join(ZIP,files)
                if(not os.path.isfile(destpath)):
                    shutil.move(filepath,ZIP)
                

def unzip_files(ZIP,EMSD):
    # ZIP: directory name containing .zip file
    # EMSD: destiantion
    current_working_dir= os.getcwd()
    for root,directory,file in os.walk(ZIP):
        for filename in file:
            zip_file_path=os.path.join(root,filename)
            with ZipFile(zip_file_path,'r') as zip:
                checkfile=os.path.join(EMSD,zip.namelist()[0])
                if(os.path.isfile(checkfile)==False):
                    zip.extractall()
                    unzip_filepath=os.path.join(current_working_dir,zip.namelist()[0])
                    shutil.move(unzip_filepath,EMSD)

def create_database_file(dest_folder, loc):
    dest = os.path.join(dest_folder,loc)
    dest = dest+".db"
    isdir=os.path.isdir(dest)
    if not isdir:
        with open(dest,"w") as f:
            return dest


def rename(dirpath):
  
    search_dir = dir
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    print(files ,'\n')
    new_name = 'CCS'+ '_' +location + '_' + sys + '_' + device + filetype
    

    if(os.path.isfile(os.path.join(search_dir,new_name))):
        os.remove(new_name)
    os.rename(files[-1], new_name)


def dictionary(item):
    split_arr = item.split('_')
    loc = split_arr[1]
    device_code = split_arr[2]
    date = int(split_arr[3])
    timestamp = int(split_arr[4])
    current_dict = {
            "loc_deviceCode" : loc +'_'+ device_code,
            "date" : date ,
            "timestampe" : timestamp
    }
    return current_dict

def getLatestFileTime(dirpath,zip_file_path):
    list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(dirpath, x)),
                        os.listdir(dirpath) ) )
    list_of_zipfiles = sorted( filter( lambda x: os.path.isfile(os.path.join(zip_file_path, x)),
                        os.listdir(zip_file_path) ) )
    total_dict = []
    need_save_file_list = []
    need_save_zip_list = []
    k = 0
    index = 0
    while index < len(list_of_files)-1 :
        ele = list_of_files[index]
        item = Path(ele).stem
        current_dict = dictionary(item)
        
        next_dict = dictionary(Path(list_of_files[index+1]).stem)
        if current_dict["loc_deviceCode"] != next_dict["loc_deviceCode"]:
            total_dict.append(current_dict)
            need_save_file_list.append(list_of_files[index])
            need_save_zip_list.append(list_of_files[index].split('.')[0] +'.zip')
        index+=1
    ele = list_of_files[index]
    item = Path(ele).stem
    current_dict = dictionary(item)
    if current_dict["loc_deviceCode"] != total_dict[-1]["loc_deviceCode"]:
        total_dict.append(current_dict)
        need_save_file_list.append(list_of_files[index])
        need_save_zip_list.append(list_of_files[index].split('.')[0]+'.zip')
    else:
        total_dict[-1] = current_dict
    for file in list_of_files:
        if file not in need_save_file_list:
            path =  dirpath+ '/' + file
            print(f"removed files : {path}")
            os.remove(path)
   
   
    for zip_file in list_of_zipfiles:
        if zip_file not in need_save_zip_list:
            path =  zip_file_path+ '/' + zip_file
            print(f"removed zip : {path}")
            os.remove(path)
            
        
       
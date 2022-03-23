import os
import shutil
from zipfile import ZipFile
import sqlite3
from sqlite3 import Error
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
                shutil.move(filepath,ZIP)

def unzip_files(ZIP,EMSD):
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

def create_database_file(dest_folder, loc_sys):
    dest = os.path.join(dest_folder,loc_sys)
    dest = dest+".db"
    isdir=os.path.isdir(dest)
    if not isdir:
        with open(dest,"w") as f:
            return dest

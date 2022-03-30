import os
from datetime import datetime
def sort_dir(dir , location,sys,device):
    search_dir = dir
    os.chdir(search_dir)
    
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    
    new_name = 'CCS'+ '_' +location + '_' + sys + '_' + device + '.zip'
    
    if(os.path.isfile(os.path.join(search_dir,new_name))):
        os.remove(new_name)
    os.rename(files[-1], new_name)
    


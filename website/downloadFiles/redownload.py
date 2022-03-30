from download import findrow, click_to_export, download_Condition
from waiting import Wait, InputField_Alltable
import selenium
from download_CCS import download_CCS
#redownload
def outputfiletype(driver, filetype):
    can_click = True
    while (can_click):
        try:
            output_files = InputField_Alltable(driver,0)[0].find_elements_by_tag_name("li")
            driver.implicitly_wait(3)
            output_files[filetype].click()
            can_click=False
        except selenium.common.exceptions.TimeoutException:
            pass
        except selenium.common.exceptions.ElementClickInterceptedException:
            pass
    return output_files
def redownload(driver, Cannot_download_index):
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
                checking=download_Condition(driver)
                if(checking[0]==False):
                    print(val[0])
                    driver.implicitly_wait(20)
                    index+=1
                else:
                    Cannot_download_index.remove(index)
    print(Cannot_download_index)
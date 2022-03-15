from selenium import webdriver
from selenium.webdriver.common.keys import Keys #enter key
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

path="D:\FYP\chromedriver.exe"
driver=webdriver.Chrome(path)
driver.get("https://orteil.dashnet.org/cookieclicker/")

driver.implicitly_wait(5)   #wait 5s before go into next line, same as wait(5)
cookie=driver.find_element_by_id("bigCookie")
cookie_count=driver.find_element_by_id("cookies")
items=[driver.find_element_by_id("productPrice"+str(i)) for i in range (1,-1,-1)]
#for(i=1;i==-1;i-1) reverse go

actions=ActionChains(driver) #perform in sequence, chain of actions
actions.click(cookie)

for i in range(5000):
    actions.perform()#only click on cookie 5000 times
    count=int(cookie_count.text.split(" ")[0])
    print(count)
    for item in items:
        value=int(item.text)
        if value<=count:
            upgrade_actions=ActionChains(driver) #new action chain
            #As item is different item, we dun know which item gonna be, need to redefine the action chain
            upgrade_actions.move_to_element(item)
            upgrade_actions.click()
            upgrade_actions.perform()
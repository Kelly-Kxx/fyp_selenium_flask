from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Wait(waiting_time, xpath, driver):
    return WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
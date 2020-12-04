from selenium import webdriver
import time


# initializing webdriver
PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://google.com")
driver.find_element_by_name("q").send_keys("Allegro")
driver.find_element_by_name("btnK").submit()
time.sleep(5)

driver.quit()
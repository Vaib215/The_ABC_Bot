from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
def calender(uid,password,id):
    driver.get('https://cuchd.blackboard.com/ultra/calendar')
    driver.find_element_by_xpath('//*[@id="agree_button"]').click()
    driver.find_element_by_xpath('//*[@id="user_id"]').send_keys(uid)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="entry-login"]').click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main-heading"]')))
    text='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta http-equiv="X-UA-Compatible" content="ie=edge">\n<title>Marks</title>\n</head>\n<body>\n'
    dues=driver.find_elements_by_class_name("due-item")
    for item in dues:
        text= text+item.get_attribute("outerHTML")+"\n"
    calender = open("{}_calender.html".format(id),"w")
    calender.write(text+"\n</body>\n</html>\n")
    calender.close()
    driver.quit()
    return "{}_calender.html".format(id)

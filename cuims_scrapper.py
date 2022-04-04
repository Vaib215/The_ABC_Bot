from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
import os
import time
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
driver.get('https://uims.cuchd.in/uims/')
driver.find_element_by_id('txtUserId').send_keys("21BCS10561")
driver.find_element_by_id('btnNext').click()
driver.find_element_by_xpath('//*[@id="txtLoginPassword"]').send_keys("UIms@123")
driver.find_element_by_id('btnLogin').click()
time.sleep(5)
while(True):
    choice = int(input("What do you want to see?\n1. Attendance\n2. Exam Marks\n3. Time Table\n4. Quit\n"))
    if choice==1:
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[1]/li[2]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="SortTable"]').screenshot("att.png")
        att=Image.open(r"att.png")
        att.show()
        att.close()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
    elif choice ==2:
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[6]/li[4]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[6]/ul[2]/li[2]/a').click()
        time.sleep(3)
        text='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><title>Marks</title></head><body>'
        subjects = driver.find_elements_by_class_name("ui-accordion-header")
        for i in range(len(subjects)):
            text = text + subjects[i].get_attribute('innerHTML')+ driver.find_element_by_id("ui-accordion-accordion-panel-"+str(i)).get_attribute('innerHTML') + "\n"
        text=text+'</body></html>'
        marks = open("marks.html",'w')
        marks.write(text)
        marks.close()
        cwd = os.getcwd()
        driver.get("file://"+cwd+"/marks.html")
        time.sleep(3)
        driver.find_element_by_tag_name("body").screenshot("marks.png")
        marks=Image.open(r"marks.png")
        marks.show()
        marks.close()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()

    elif choice==3:
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[1]/li[4]/a').click()
        time.sleep(3)
        driver.find_element_by_id('ContentPlaceHolder1_gvMyTimeTable').screenshot("TimeTable.png")
        tt = Image.open(r"TimeTable.png")
        tt.show()
        tt.close()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
    else:
        print("Thanks for using me!")
        driver.quit()
        break
        
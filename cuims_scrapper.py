from selenium import webdriver
import bb
import os
import time
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
def login(uid,password):
    driver.get('https://uims.cuchd.in/uims/')
    driver.find_element_by_id('txtUserId').send_keys(uid)
    driver.find_element_by_id('btnNext').click()
    driver.find_element_by_xpath('//*[@id="txtLoginPassword"]').send_keys(password)
    driver.find_element_by_id('btnLogin').click()
def utility(uid,password,id,choice):
    if choice=="1" or choice=="attendance":
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[1]/li[2]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="SortTable"]').screenshot("{}_attendance.png".format(id))
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
        return "{}_attendance.png".format(id)
    elif choice =="2" or choice=="marks":
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[6]/li[4]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[6]/ul[2]/li[2]/a').click()
        time.sleep(3)
        text='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><title>Marks</title></head><body>'
        subjects = driver.find_elements_by_class_name("ui-accordion-header")
        for i in range(len(subjects)):
            text = text + subjects[i].get_attribute('innerHTML')+ driver.find_element_by_id("ui-accordion-accordion-panel-"+str(i)).get_attribute('innerHTML') + "\n"
        text=text+'</body></html>'
        marks = open("{}_marks.html".format(id),'w')
        marks.write(text)
        marks.close()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()
        return "{}_marks.html".format(id)
    elif choice=="3" or choice=="timetable":
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[1]/li[4]/a').click()
        time.sleep(3)
        driver.find_element_by_id('ContentPlaceHolder1_gvMyTimeTable').screenshot("{}_timeTable.png".format(id))
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[1]/a').click()
        return "{}_timeTable.png".format(id)
    elif choice=="4" or choice=="calender":
        return bb.calender(uid,password,id)
    elif choice=="5" or choice=="datesheet":
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[6]/li[1]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_wucStudentDateSheet_gvStudentDateSheet"]').screenshot("{}_datesheet.png".format(id))
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()
        return "{}_datesheet.png".format(id)
    elif choice=="6" or choice=="result":
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[6]/li[2]/a').click()
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/ul[6]/ul[1]/li/a').click()
        driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_wucResult1_dvResult"]').screenshot("{}_result.png".format(id))
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[11]/a').click()
        return "{}_result.png".format(id)
    elif choice=="7" or choice=="profile":
        driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/ul/li[13]/a').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ReportViewer1_fixedTable"]').screenshot("{}_profile.png".format(id))
        return "{}_profile.png".format(id)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import sys
import datetime
import calendar
import pytz
tz_IN = pytz.timezone('Asia/Kolkata')   
curr_date = datetime.date.today()
week = calendar.day_name[curr_date.weekday()]
now=datetime.datetime.now(tz_IN)
hr=now.hour
mn=now.minute
path=0
curtime= time.time()
#Subjects
digitalElec = 'https://cuchd.blackboard.com/ultra/courses/_65091_1/outline' #DE
physics = 'https://cuchd.blackboard.com/ultra/courses/_62252_1/outline' #Physics
communication = 'https://cuchd.blackboard.com/ultra/courses/_62699_1/outline' #CS
maths = 'https://cuchd.blackboard.com/ultra/courses/_61177_1/outline' #Maths
lsm = 'https://cuchd.blackboard.com/ultra/courses/_60610_1/outline' #LSM
oops = 'https://cuchd.blackboard.com/ultra/courses/_61876_1/outline' #OOPS
dt = 'https://cuchd.blackboard.com/ultra/courses/_58794_1/outline' #DT
indepPro = 'https://cuchd.blackboard.com/ultra/courses/_59801_1/outline' #Independent
cgcad = 'https://cuchd.blackboard.com/ultra/courses/_57926_1/outline' #CGCAD
ipr = 'https://cuchd.blackboard.com/ultra/courses/_65727_1/outline' #IPR

if week=="Monday":
    if hr==9 or hr==10:
        path = communication
    elif hr==11:
        path= digitalElec
    elif hr==12:
        path= maths
    elif hr==14 and mn<=40:
        path = oops
    elif hr==14 and mn>=50 or hr==15 and mn<=30:
        path = maths
    elif hr==15 and mn>=40 or hr==16:
        path=ipr
elif week=="Tuesday":
    if hr==9 or hr==10 or hr==11:
        path= digitalElec
    elif hr==12:
        path=physics
    elif hr==14 or (hr==15 and mn<=30):
        path = physics
    elif hr==15 and mn>=40:
        path=communication
elif week=="Wednesday":
    if hr==9:
        path = physics
    elif hr==10:
        path= oops
    elif hr==11:
        path= maths
    elif hr==13 or (hr==14 and mn<=40):
        path= oops
    elif hr==14 or hr==15:
        path= communication
elif week=="Thursday":
    if hr==9 or hr==10 or (hr==11 and mn<=10):
        path = cgcad
    elif hr == 13 or (hr==14 and mn<=40):
        path = dt
    elif hr == 14 or (hr==15 and mn<=30):
        path = physics
    elif hr == 15 and mn>=40:
        path=lsm
elif week =="Friday":
    if hr ==9:
        path= indepPro
    elif hr==10:
        path= digitalElec
    elif hr==11:
        path= maths
    elif hr==13:
        path= dt
    elif hr==14 or hr==15:
        path=oops

if path:
    ## Variables
    URL = path
    UID = '21BCS10561'
    PASSW = 'UIms@123'
    ERR_STRINGS =["Loading failed. Exiting...","Joining Session Failed. Exiting...","Loading of Audio Test Page failed. Exiting...","Audio Test failed. Exiting...","Something went wrong while Cleaning Screen. Exiting...","Camera Test Failed. Exiting..."]
    T_UNTIL_LEAVE = 40
    T_UNTIL_LEAVE = 60*T_UNTIL_LEAVE
    WARNINGS = []

    ## Functions

    ## 1. Configure Firefox Preferences
    def new_foxfire():
        p = webdriver.FirefoxProfile()
        p.set_preference("permissions.default.microphone", 1) #Allow mic access
        p.set_preference("permissions.default.camera", 1) # Allow cam access
        p.set_preference("media.volume_scale", "0.0") #Muting the tab
        p.update_preferences()
        return p
    ## 2. Configure Headless Mode
    def new_foxfire_options():
        n = Options()
        n.headless = True
        return n
    ## 3. Safely Check if an element is visible
    def waitforexec(arg1, arg2, arg3=30,arg4=False):
        try:
            found = WebDriverWait(driver, arg3).until(EC.visibility_of_element_located((By.XPATH,arg1)))
            if (arg4 == True):
                return found
        except TimeoutException:
            term(arg2)
    ## 4. Terminate Script w Reason.
    def term(reason):
        driver.quit()
        sys.exit(reason)

    def warn_user(text): # Reduce terminal spam.
        s = len(WARNINGS)
        if (s ==0):
            WARNINGS.append(text)
            print(WARNINGS[0])
        elif(WARNINGS[s-1] != text):
            WARNINGS.append(text)
            print(WARNINGS[len(WARNINGS)-1])
    ## 5. Clean up BB UI

    def cleanupUI():
        a = waitforexec("//button[@analytics-id='announcement.introduction.later']",ERR_STRINGS[5],30,True)
        time.sleep(5)
        a.click()
        b = waitforexec("//button[@analytics-id='tutorial.finish']","Tutorial Finish Btn not found.",30,True)
        time.sleep(5)
        b.click()
        try:
            side = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//button[@id='side-panel-open']")))
            time.sleep(5)
            side.click()
        except:
            term("Sidepanel btn couldn't be selected.")
        c = waitforexec("//li[@id='panel-control-participants']","Could find participants tab.",30,True)
        time.sleep(5)
        c.click()
        print("Cleared up UI.")


    ## 8. Check if people have left the session.
    def check_decrease():
        print("Waiting for "+str(T_UNTIL_LEAVE)+"s")
        while(time.time() < curtime+T_UNTIL_LEAVE):
            time.sleep(5)
        term("Class Time finished!")

    #Launch GeckoDriver with custom prefs.
    print("Launching Firefox...")
    driver = webdriver.Firefox(options=new_foxfire_options(), firefox_profile=new_foxfire())

    print("Loading BlackBoard Join Page...")
    driver.get(URL)
    agree=waitforexec('//*[@id="agree_button"]',"Agree Button Not Found",30,True)
    agree.click()
    id1 = waitforexec('//*[@id="loginFormList"]/li[1]/label',"can't find",30,True)
    id1.click()
    id2 = waitforexec('//*[@id="user_id"]',"Can't add user name",30,True)
    id2.send_keys(UID)
    passw = waitforexec('//*[@id="password"]',"Can't add password",30,True)
    passw.send_keys(PASSW)
    login = waitforexec('//*[@id="entry-login"]',"Can't login",30,True)
    login.click()
    print("Finding Current Class")
    link = waitforexec('//*[@id="sessions-list-dropdown"]/span',"Can't find any class",30,True)
    link.click()
    openclass = waitforexec('//*[@id="sessions-list"]/li/a',"Can't find any class",30,True)
    if(openclass.text=='Course Room'):
        print("First class is Course Room. Selecting 2nd one.")
        openclass=waitforexec('//*[@id="sessions-list"]/li[2]/a',"Can't find any class",30,True)
    openclass.click()
    time.sleep(5)
    print("Class Started")
    driver.switch_to.window(driver.window_handles[1])
    waitforexec("//p[@analytics-id='session.connection-status.user-joining-session']",ERR_STRINGS[1])
    time.sleep(10)
    driver.execute_script('document.querySelectorAll("button.close")[3].click()')
    waitforexec("//h2[@analytics-id='announcement.introduction.title']", ERR_STRINGS[1],50)
    print("You have joined the class!")

    cleanupUI()
    check_decrease()
else:
    print("No class right now")

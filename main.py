import telebot
from telebot.types import Message
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

API_KEY = '5275003138:AAGNa-myKUUYkA6Uc9LK0sZSwllGK6XP3bs'

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(message, "Welcome to UIMS Attendance Bot!\nPlease send me your UIMS username.")

@bot.message_handler(func=lambda message: True)
def get_username(message: Message):
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--maximize-window')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.wait = WebDriverWait(driver, 10)
    username = message.text.strip()
    bot.reply_to(message, "Great! Now, please send me your UIMS password.")
    bot.register_next_step_handler(message, get_password, username, driver)

def get_password(message: Message, username: str, driver: webdriver.Chrome):
    password = message.text.strip()
    bot.reply_to(message, "Thanks! Logging in...")
    login(username, password,driver)
    bot.send_photo(message.chat.id, open('captcha.png', 'rb'))
    bot.reply_to(message, "Please send me the CAPTCHA shown above.")
    bot.register_next_step_handler(message, get_captcha_from_user, driver)

def get_captcha_from_user(message: Message, driver: webdriver.Chrome):
    captcha = message.text.strip()
    bot.reply_to(message, "Thanks! Fetching attendance...")
    attendance = fetch_attendance(driver, captcha)
    bot.send_message(message.chat.id, attendance)

def login(username: str, password: str, driver: webdriver.Chrome) -> None:
    try:
        driver.get('https://uims.cuchd.in/uims/')
        driver.find_element(By.NAME, 'txtUserId').send_keys(username)
        driver.find_element(By.NAME, 'btnNext').click()
        driver.find_element(By.NAME, 'txtLoginPassword').send_keys(password)
        captcha = driver.find_element(By.ID, 'imgCaptcha').screenshot('captcha.png')
        return

    except Exception as e:
        pass

def fetch_attendance(driver: webdriver.Chrome, captcha: str) -> str:
    try:
        driver.find_element(By.NAME, 'txtcaptcha').send_keys(captcha)
        driver.find_element(By.NAME, 'btnLogin').click()
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, 'divForcePopUp')))
        driver.execute_script("document.getElementById('divForcePopUp').remove();")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.modal-backdrop.fade.in')))
        driver.execute_script("document.querySelector('.modal-backdrop.fade.in').remove();")
        wait.until(EC.presence_of_element_located((By.ID, 'txtUserSearch001_PC')))
        attendance_table = driver.find_element(By.CSS_SELECTOR, '#div-subject-details table')
        rows = attendance_table.find_elements(By.TAG_NAME, 'tr')
        attendance = ""
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) > 0:
                attendance += f"{cols[0].text} - {cols[2].text}\n"
            
        return str(attendance)

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    bot.polling()

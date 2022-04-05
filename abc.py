from telegram import *
from telegram.ext import *
import credentials
import cuims_scrapper
bot = Bot(credentials.bot_token)

updater = Updater(credentials.bot_token,use_context=True)
dispatcher = updater.dispatcher
def showDefMessage(update):
  update.message.reply_text("First login by /login then send\n1 for attendance\n2 for Marks\n3 for Timetable")

def start(update:Update, context):
  username = update['message']['chat']['first_name']   
  chat_id = update.message.chat_id
  update.message.reply_text("Hello, if you are here for first time then /addCredentials first.")
  showDefMessage(update)
ONE , TWO = range(2)
def add_credentials(update: Update, context: CallbackContext):
     chat_id = update.message.chat_id
     bot.send_message(chat_id , text = "hello , you are registering ! please enter your UID | type 'cancel' anytime to cancel process")
     return ONE

def got_uid(update: Update, context: CallbackContext):
     chat_id = update.message.chat_id
     uid = update.message.text # now we got the UID
     context.user_data["uid"] = uid # to use it later (in next func)
     bot.send_message(chat_id , text = f"Enter password for UID {uid}:")
     return TWO
def saveData(uid,password,id):
  cred = open("{}.txt".format(id),"w")
  cred.write("{}\n{}".format(uid,password))
  cred.close()
def got_password(update: Update, context: CallbackContext):
     chat_id = update.message.chat_id
     password = update.message.text # now we got the password
     uid = context.user_data["uid"] # we had the name , remember ?!
     context.user_data["password"] = password
     saveData(uid,password,chat_id)
     bot.send_message(chat_id , text = f"completed ! your name is {uid} and your phone number is {password}")
     return ConversationHandler.END
def cancel(update: Update, context: CallbackContext):
     chat_id = update.message.chat_id
     bot.send_message(chat_id , text = "process canceled !")
     return ConversationHandler.END
CH = ConversationHandler (entry_points = [CommandHandler("addCredentials", add_credentials)],
     states = {ONE : [MessageHandler(Filters.text , got_uid)],
     TWO : [MessageHandler(Filters.text , got_password)]
     },
     fallbacks = [MessageHandler(Filters.regex('cancel'), cancel)],
     allow_reentry=  True)
def main_handler(update, context:CallbackContext):
  update:Update
  choice = update.message.text
  chat_id = update.message.chat_id
  file=cuims_scrapper.utility(chat_id,choice)
  bot.send_document(chat_id,open(file,'rb'))
def login(update:Update,context:CallbackContext):
  chat_id = update.message.chat_id
  try:
    bot.send_message(chat_id,"Logging in, wait for few seconds.")
    cred = open("{}.txt".format(chat_id))
    text = cred.read()
    uid,password = text.split()
    cred.close()
    cuims_scrapper.login(uid,password)
    bot.send_message(chat_id,"Successfully logged in")
  except:
    bot.send_message(chat_id,"No Credentials Found. Add Credentials by /addCredentials .")
dispatcher.add_handler(CH)
dispatcher.add_handler(CommandHandler('login',login))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, main_handler)) 
updater.start_polling()
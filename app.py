import logging
from flask import Flask, request
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

#create a custom logger
logger = logging.getLogger(__name__)

# telegram bot taken
TOKEN = "1432780373:AAFYXpaonmaRH_eIrdYnYtm58OcDWOkisD0"

# app object for using flask
app = Flask(__name__)

# This is for testing purpose only
@app.route('/')
def index():
    return "Hello!"

# view to handle webhooks
@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
   # webhook view which receives updates from telegram
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"



# By default any function pass inside command handler it will get to arguments
def start(bot,update):
   # callback function for /start handler
    # print(update)
    author = update.message.from_user.first_name # who has send me /sart command
    reply = "Hi! {}".format(author) # reply hi to author
    bot.send_message(chat_id=update.message.chat_id,text=reply) # send reply text to bot

def _help(bot,update):
   # callback function for /help handler
    help_txt="Hey! This is a help text."
    bot.send_message(chat_id=update.message.chat_id,text=help_txt)

def news(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text="Choose a category",
    reply_markup = ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True))

def reply_text(bot,update):
   # callback function for text message handler
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        # reply_text = "Ok! I will show you news with {}".format(reply)
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot,update):
   # callback function for sticker message handler
    bot.send_sticker(chat_id=update.message.chat_id,
    sticker=update.message.sticker.file_unique_id)

def error(bot,update):
   # callback function for error handler
    logger.error("Update '%s' caused error '%s'", update, update.error) 
 
bot = Bot(TOKEN)  # meake bot object not require updater as not polling program
try:
    bot.set_webhook("https://3d9961f0f6c7.ngrok.io/"+TOKEN) # set webhook for telegram bot
except Exception as e:
    print(e)

dp = Dispatcher(bot,None) # new Dispatcher function is required

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)


# creating entry point for my program
if __name__ == "__main__":  
    app.run(port = 8443)






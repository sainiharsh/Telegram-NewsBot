import logging
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

#create a custom logger
logger = logging.getLogger(__name__)

# telegram bot taken
TOKEN = "1432780373:AAFYXpaonmaRH_eIrdYnYtm58OcDWOkisD0"

# By default any function pass inside command handler it will get to arguments
def start(bot,update):
   # """callback function for /start handler"""
    print(update)
    author = update.message.from_user.first_name # who has send me /sart command
    reply = "Hi! {}".format(author) # reply hi to author
    bot.send_message(chat_id=update.message.chat_id,text=reply) # send reply text to bot

def _help(bot,update):
   # """callback function for /help handler"""
    help_txt="Hey! This is a help text."
    bot.send_message(chat_id=update.message.chat_id,text=help_txt)

def echo_text(bot,update):
   # """callback function for text message handler"""
    reply = update.message.text
    bot.send_message(chat_id=update.message.chat_id,text=reply)

def echo_sticker(bot,update):
   # """callback function for sticker message handler"""
    bot.send_sticker(chat_id=update.message.chat_id,
    sticker=update.message.sticker.file_unique_id)

def error(bot,update):
   # """callback function for error handler"""
    logger.error("Update '%s' caused error '%s'", update, update.error) 

def main():
# Updater receives update from telegram send to dispatcher.
    updater = Updater(TOKEN)
# Dispatcher handle the updates as it has many handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)

    updater.start_polling()
    logger.info("Started Polling....")
    updater.idle()  # waits until the user press Ctrl+c or anything to stop 


# creating entry point for my program
if __name__ == "__main__":
    main()







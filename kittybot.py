from multiprocessing import context
import requests
import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

load_dotenv()

updater = Updater(token=os.getenv('TOKEN'))
URL = os.getenv('URL')


def get_new_image():
    try:
        response=requests.get(URL,verify=False)
    except Exception as error:
        print(error)
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url,verify=False)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Увидеть кота!']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашел!'.format(name),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())

updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

updater.start_polling()
updater.idle()

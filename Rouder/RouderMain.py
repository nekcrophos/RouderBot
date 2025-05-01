from telebot import types
import telebot
import os
from dotenv import load_dotenv
from handlers import confirmation_InfoHandler, introductionHandler

load_dotenv()
token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)

class User:
    def __init__(self):
        self.id = None
        self.name = None
        self.surname = None
        self.age = 0

users = {}

with open('introduction.txt', 'r', encoding='utf-8') as f:
    introduction = f.read()

with open('pream.txt', 'r', encoding='utf-8') as f:
    preamble = f.read()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, introduction)
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('Да', callback_data='yes_indeed'),
        types.InlineKeyboardButton('Нет', callback_data='no_imnot')
    )
    bot.send_message(message.chat.id, preamble, reply_markup=keyboard)

for x in os.listdir("./handlers/"): # looking for files in ./handlers/ folder
    if x.endswith(".py"): # ignore non-python files
        cog = __import__("handlers." + x[:-3]) # import is a built-in python function that allows dynamic imports
         # x[:-3] removes ".py" at the end of the files' names       
        cog.run(bot) # run cog, so all handlers in it will be registered on a bot Telebot instance


if __name__ == '__main__':
    bot.polling(none_stop=True)
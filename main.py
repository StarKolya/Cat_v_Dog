from telebot import TeleBot, types
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('BOT_TOKEN')
bot = TeleBot(token=token)


user_images = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "This bot is designed for practice purposes only."
                     "It accepts an image and sends an API request to Hugging Face, "
                     "where my custom-built Neural Network is hosted.")


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    file_id = message.photo[-1].file_id
    user_images[message.chat.id] = file_id
    bot.send_message(message.chat.id, "Image received and stored!")


@bot.message_handler(func=lambda message: True)
def handle_non_image(message):
    if message.chat.id in user_images:
        file_id = user_images[message.chat.id]
        bot.send_photo(message.chat.id, file_id)
    else:
        bot.send_message(message.chat.id, "I only accept images of cats or dogs. Please send one!")


bot.polling()
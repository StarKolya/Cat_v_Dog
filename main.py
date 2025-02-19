from telebot import TeleBot, types
from dotenv import load_dotenv
from gradio_client import Client, handle_file
import os
import json

load_dotenv()

token = os.getenv('BOT_TOKEN')
bot = TeleBot(token=token)

# Dictionary to store user images
user_images = {}

# Initialize Gradio client
client = Client("StarKolya/FirstSpace")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Send me an image of a cat or dog. I will store it for you and process it!")

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_path = f"{message.chat.id}_image.jpg"
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        user_images[message.chat.id] = file_path
        bot.send_message(message.chat.id, "Image received and stored! Processing it now...")

        # Send image to Hugging Face Space
        result = client.predict(
            img=handle_file(file_path),
            api_name="/predict"
        )
        if result["confidences"][0]["label"] == "dog":
            dog_result = round(result["confidences"][0]["confidence"], 3) * 100
            cat_result = round(result["confidences"][1]["confidence"], 3) * 100
        else:
            dog_result = round(result["confidences"][1]["confidence"], 3) * 100
            cat_result = round(result["confidences"][0]["confidence"], 3) * 100

        bot.send_message(message.chat.id, f"Based on the photo provided, the probability that it is:\n"
                                        f"A dog: {dog_result}%\n"
                                        f"A cat: {cat_result}%")

        if dog_result > cat_result:
            bot.send_message(message.chat.id, f"I think that it is a <b>Dog!</b>", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, f"I think that it is a <b>Cat!</b>", parse_mode="HTML")

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while processing the image: {str(e)}")

@bot.message_handler(func=lambda message: True)
def handle_non_image(message):
    bot.send_message(message.chat.id, "I only accept images of cats or dogs. Please send one!")

bot.polling()

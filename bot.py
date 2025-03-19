from flask import Flask, request
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from scrap import name, price
import os

API_ID = '23656786'
API_HASH = '8860726fc74c156164ff8478d11f9375'
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]  # Use environment variable

app = Flask(__name__)
bot = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.route('/api/bot', methods=['POST'])
def webhook():
    update = request.get_json()
    bot.process_update(update)
    return "OK"

@bot.on_message(filters.command("start"))  # Responds to the /start command
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("دریافت قیمت ارز دیجیتال", callback_data="get_price")]
    ])
    await client.send_message(message.chat.id, "به ربات خوش آمدید! برای دریافت قیمت ارز دیجیتال دکمه زیر را فشار دهید:", reply_markup=keyboard)

@bot.on_callback_query(filters.regex("get_price"))
async def get_price(client, callback_query):
    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(name[i], callback_data=f"price_{i}") for i in range(0, 3)],
            [InlineKeyboardButton(name[i], callback_data=f"price_{i}") for i in range(3, 6)],
            [InlineKeyboardButton(name[i], callback_data=f"price_{i}") for i in range(6, 9)],
            [InlineKeyboardButton(name[i], callback_data=f"price_{i}") for i in range(9, 12)],
            [InlineKeyboardButton(name[i], callback_data=f"price_{i}") for i in range(12, 15)],
            [InlineKeyboardButton(name[i], callback_data=f"price_{i}") for i in range(15, 18)]
    ])
    await callback_query.answer()  # Acknowledge the button press
    await client.send_message(callback_query.message.chat.id, "لطفاً ارز دیجیتال مورد نظر خود را انتخاب کنید:", reply_markup=keyboard)

@bot.on_callback_query(filters.regex("price_(\d+)"))
async def show_price(client, callback_query):
    index = int(callback_query.data.split("_")[1])
    selected_price = price[index]
    await callback_query.answer()  # Acknowledge the button press
    await client.send_message(callback_query.message.chat.id, f"قیمت ارز {name[index]}: {selected_price} \n به شما نشان داده شد.")

@app.route('/')
def home():
    return "Telegram Bot is running!"

if __name__ == "__main__":
    bot.start()
    app.run(debug=True)

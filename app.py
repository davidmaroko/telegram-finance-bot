from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing! Check your environment variables.")

print(f"Loaded TELEGRAM_BOT_TOKEN: {TOKEN[:10]}...")  # הדפסה חלקית לבדיקה

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return '', 200

@app.route('/')
def home():
    return "The bot is running on Render!", 200

# טיפול בהודעות טלגרם
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "שלום! אני מחובר לאתר שלך.")

# טיפול בכל הודעה שנשלחת לבוט
@bot.message_handler(func=lambda message: True)  # מתייחס לכל הודעה
def echo_all(message):
    response = f"תשובה: {message.text}"  # מוסיף את הקידומת "תשובה:"
    bot.send_message(message.chat.id, response)  # שולח חזרה את ההודעה

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # שימוש בפורט דינמי
    app.run(host="0.0.0.0", port=port, debug=True)

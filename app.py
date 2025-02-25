# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route("/")
# def home():
    # return "Telegram Finance Bot is Running!"

# @app.route("/webhook", methods=["POST"])
# def webhook():
    # data = request.json
    # print(f"Received data: {data}")  # לצורך בדיקה
    # return jsonify({"status": "received"}), 200

# if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000)

import os
from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

app = Flask(__name__)

# קבלת הטוקן מה-Environment Variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# רשימת משתמשים מאושרים (הכנס את ה-Chat ID שלך ושל אחרים)
AUTHORIZED_USERS = {6406831521}  # הכנס את ה-Chat IDs כאן

# דף הבית לבדיקה
@app.route("/")
def home():
    return "Telegram Finance Bot is Running!", 200

# Webhook לטלגרם
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return jsonify({"status": "received"}), 200

# פונקציה שמופעלת כשמשתמש שולח הודעה לבוט
def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    # בדיקה אם המשתמש רשאי להשתמש בבוט
    if chat_id not in AUTHORIZED_USERS:
        bot.send_message(chat_id=chat_id, text="❌ אין לך הרשאה להשתמש בבוט הזה.")
        return

    response = f"התקבלה הודעה: {text}"
    bot.send_message(chat_id=chat_id, text=response)

# אתחול ה-Dispatcher (מנהל האירועים של הבוט)
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

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
from telegram.ext import Application, MessageHandler, filters, CallbackContext

app = Flask(__name__)

# קבלת הטוקן מה-Environment Variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# יצירת Application
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# רשימת משתמשים מורשים (החלף ב-Chat IDs האמיתיים שלך)
AUTHORIZED_USERS = {6406831521}  # הכנס כאן את ה-Chat ID של המשתמשים המורשים

# דף הבית לבדיקה
@app.route("/")
def home():
    return "Telegram Finance Bot is Running!", 200

# Webhook לטלגרם
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"Received update: {data}")  # הדפסה ללוגים
    update = Update.de_json(data, bot)
    application.process_update(update)
    return jsonify({"status": "received"}), 200



# פונקציה שמופעלת כשמשתמש שולח הודעה לבוט
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    # בדיקה אם המשתמש רשאי להשתמש בבוט
    if chat_id not in AUTHORIZED_USERS:
        await bot.send_message(chat_id=chat_id, text="❌ you are not allowed to use this bot.")
        return

    response = f"התקבלה הודעה: {text}"
    await bot.send_message(chat_id=chat_id, text=response)

# הוספת ה-Handler החדש
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


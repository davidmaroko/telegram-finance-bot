import os
import logging
from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# הפעלת לוגים מפורטים
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# קבלת הטוקן מה-Environment Variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# יצירת Application
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# רשימת משתמשים מורשים
AUTHORIZED_USERS = {6406831521}  # הכנס כאן את ה-Chat ID של המשתמשים המורשים

# דף הבית לבדיקה
@app.route("/")
def home():
    return "Telegram Finance Bot is Running!", 200

# Webhook לטלגרם  
@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json()
    logging.info(f"Received update: {data}")  # הדפסת הנתונים ללוגים

    try:
        # ודא שה-Update מכיל "message" לפני עיבודו
        if "message" in data:
            update = Update.de_json(data, bot)
            await application.process_update(update)  # הוספנו await
            logging.info("Message processed successfully.")
        else:
            logging.warning("Skipping update, no 'message' key found.")

        return jsonify({"status": "received"}), 200
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# פונקציה שמופעלת כשמשתמש שולח הודעה לבוט
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    logging.info(f"Received message from {chat_id}: {text}")

    # בדיקה אם המשתמש רשאי להשתמש בבוט
    if chat_id not in AUTHORIZED_USERS:
        logging.warning(f"Unauthorized user {chat_id} tried to access the bot.")
        await bot.send_message(chat_id=chat_id, text="❌ you are not allowed to use this bot.")
        return

    response = f"התקבלה הודעה: {text}"
    await bot.send_message(chat_id=chat_id, text=response)
    logging.info(f"Sent response to {chat_id}")

# הוספת ה-Handler החדש
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

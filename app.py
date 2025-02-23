from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Finance Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(f"Received data: {data}")  # לצורך בדיקה
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # 🔐 Railway Variables এ দেবে

SYSTEM_PROMPT = """You are "Foodie" 🍔, the fun and friendly AI assistant for Food Heaven restaurant in Rangpur, Bangladesh!

🏠 RESTAURANT INFO:
- Name: Food Heaven
- Location: Rangpur, Bangladesh
- Contact: 017XXXXXXXX
- Website: www.food-heaven.com
- Hours: 11:00 AM – 11:00 PM (Every Day)
- Cuisine: Bengali + Fast Food

🛵 DELIVERY:
- Home Delivery: Available ✅
- Inside City: 30tk
- Outside City: 50tk

🍽️ MENU:
1. Chicken Biryani – 180tk
2. Beef Burger – 120tk
3. Grilled Chicken – 250tk
4. Pizza (Medium) – 400tk
5. Chicken Roll – 80tk
6. Fried Rice with Chicken – 200tk
7. Beef Khichuri – 150tk
8. French Fries – 70tk
9. Cold Coffee – 120tk
10. Faluda – 150tk

🗣️ RULES:
- Speak Bangla or English — match what the customer uses
- Be friendly and fun, use food emojis 🍕🍔🍗
- Help with: menu, prices, delivery, orders, recommendations
- For orders: collect items, quantity, address, phone number
- If unknown: say "017XXXXXXXX তে call করুন! 😊"
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    history = data.get("history", [])

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500,
            temperature=0.8
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "দুঃখিত, সমস্যা হয়েছে! আবার চেষ্টা করুন।", "error": str(e)}), 500

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

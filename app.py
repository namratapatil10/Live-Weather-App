from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather")
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City name required"})

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        return jsonify({"error": data.get("message", "API Error")})

    output = {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

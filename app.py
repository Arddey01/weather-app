from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import requests

load_dotenv("weather_api/weather_api_key.env")
weather_api = os.environ.get("weather_api_key")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
app = Flask(__name__)


def get_weather(city, unit="C"):
    params = {
        "q": city,
        "appid": weather_api,
        "units": "metric" if unit == "C" else "imperial"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()
        print("STATUS:", response.status_code)
    except requests.exceptions.RequestException:
        return None

    if response.status_code != 200:
        return None

    return {
        "city": data['name'],
        "temp": data['main']["temp"],
        "description": data["weather"][0]["description"]
    }


@app.route("/", methods=["GET", "POST"])
def home():
    city = None
    unit = "C"
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        unit = request.form.get("unit", "C")

        if not city:
            error = "Please enter a city name."
        else:
            weather = get_weather(city, unit)
            if weather is None:
                error = "Couldn't fetch weather data."

    return render_template("index.html", city=city, unit=unit, weather=weather, error=error)


if __name__ == "__main__":
    app.run(debug=True)
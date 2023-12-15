from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api_key = os.getenv("API_KEY")
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city_input"]
        weather_data = get_weather(city)
        print("weather", weather_data)
        return render_template("index.html", weather_data=weather_data)
    return render_template("index.html")

def get_weather(city):
    weather_geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response_geo = requests.get(weather_geo_url)
    geo_data_response = response_geo.json()
    lat = geo_data_response[0]['lat']
    lon = geo_data_response[0]['lon']
    weather_data_url = f"https://api.openweathermap.org/data//2.5/forecast?units=imperial&lat={lat}&lon={lon}&appid={api_key}"
    response_weather = requests.get(weather_data_url)
    weather_data_response = response_weather.json()
    weather_data_json = {
        "city": geo_data_response[0]["name"],
        "temperature": f'Temp {weather_data_response["list"][0]["main"]["temp"]}F',
        "wind": f'Wind {weather_data_response["list"][0]["wind"]["speed"]} MPH',
        "humid": f'Humidity {weather_data_response["list"][0]["main"]["humidity"]}',
        "icon": f'https://openweathermap.org/img/w/{weather_data_response["list"][0]["weather"][0]["icon"]}.png'
    }
    return weather_data_json
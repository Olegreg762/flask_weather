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
        city = request.form["city"]
        weather_data = get_weather_data(city)
        return render_template("index.html", weather_data=weather_data)
    return render_template("index.html")

def get_weather_data(city):
    weather = ""
    return weather
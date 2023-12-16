from flask import Flask, render_template, request, session
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
api_key = os.getenv("API_KEY")

@app.before_request
def before_request():
    if 'history' not in session:
        session['history'] = {}
    if 'counter' not in session:
        (session['counter']) = int(0)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city_input"]
        weather_data = {'city': city, 'temperature': 'Temp 44.13F', 'wind': 'Wind 6.38 MPH', 'humid': 'Humidity 67', 'icon': 'https://openweathermap.org/img/w/04n.png'}
        # weather_data = get_weather(city)
        update_session_variables(city)
        history = session['history']
        # print(history)
        return render_template("index.html", weather_data=weather_data, history=history)
    weather_data = {'city': "New York", 'temperature': 'Temp 44.13F', 'wind': 'Wind 6.38 MPH', 'humid': 'Humidity 67', 'icon': 'https://openweathermap.org/img/w/04n.png'}
    # weather_data = get_weather('Chicago')
    return render_template("index.html",weather_data=weather_data)

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

def update_session_variables(city):
    session['history'][session['counter']].update({'visibility': 'visible', 'city': city})
    print(session)
    session['counter'] += 1
    if session['counter'] > 4:
        session["counter"] = 0
    


if __name__ == "__main__":
    app.run(port=8000, debug=True)
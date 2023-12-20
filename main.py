from flask import Flask, render_template, request, session
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
api_key = os.getenv("API_KEY")

@app.before_request
def before_request():
    if 'history' not in session:
        session['history'] = {
            0: {'visibility': 'invisible', 'city': ''},
            1: {'visibility': 'invisible', 'city': ''},
            2: {'visibility': 'invisible', 'city': ''},
            3: {'visibility': 'invisible', 'city': ''},
            4: {'visibility': 'invisible', 'city': ''}
        }
    if 'counter' not in session:
        session['counter'] = int(0)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city_input"]
        weather_data = get_weather(city)
        update_session_variables(city)
        history = session['history']
        return render_template("index.html", weather_data=weather_data, history=history)
    weather_data = get_weather('Chicago')
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
    weather_data_json = {}
    for i in range(6):
        jd = i * 8
        if jd == 40:
            jd -= 1
        date = datetime.utcfromtimestamp(weather_data_response["list"][jd]["dt"])
        formatted_date = date.strftime("%m/%d/%Y")
        weather_data_json.update({
        f"city{i}": geo_data_response[0]["name"],
        f"date{i}" : formatted_date,
        f"temperature{i}": f'Temp {weather_data_response["list"][jd]["main"]["temp"]}F',
        f"wind{i}": f'Wind {weather_data_response["list"][jd]["wind"]["speed"]} MPH',
        f"humid{i}": f'Humidity {weather_data_response["list"][jd]["main"]["humidity"]}',
        f"icon{i}": f'https://openweathermap.org/img/w/{weather_data_response["list"][jd]["weather"][0]["icon"]}.png'
        })
    print(weather_data_json)
    return weather_data_json

def update_session_variables(city):
    counter = str(session['counter'])

    history = session['history']
    history[counter].update({'visibility': 'visible', 'city': city})

    counter = int(counter)
    counter += 1
    session['counter'] += 1
    if counter > 4:
        counter = 0
        session['counter'] = 0
    


if __name__ == "__main__":
    app.run(port=8000, debug=True)
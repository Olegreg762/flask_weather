from flask import Flask, render_template, request, session
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from data.us_regions import us_regions

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
api_key = os.getenv("API_KEY")

@app.before_request
def before_request():
    if 'history' not in session:
        session['history'] = {
            0: {'visibility': 'invisible', 'city': '', 'region': ''},
            1: {'visibility': 'invisible', 'city': '', 'region': ''},
            2: {'visibility': 'invisible', 'city': '', 'region': ''},
            3: {'visibility': 'invisible', 'city': '', 'region': ''},
            4: {'visibility': 'invisible', 'city': '', 'region': ''}
        }
    if 'counter' not in session:
        session['counter'] = int(0)



@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        if 'history_input' in request.args:
            city, region = request.args['history_input'].split(',')
            return history_button(city, region)
        elif 'city_input' in request.args:
            city = request.args["city_input"].title()
            region = request.args["region_select"]
            return search_input(city, region) 
            
    weather_data = get_weather('Chicago', 'illinois')
    history = session['history']
    return render_template("index.html",weather_data=weather_data, history=history, options=us_regions)


def search_input(city,region):
    weather_data = get_weather(city, region)
    update_session_variables(city, region)
    history = session['history']
    return render_template("index.html", weather_data=weather_data, history=history, options=us_regions)


def history_button(city, region):
    weather_data = get_weather(city, region)
    history = session['history']
    return render_template("index.html", weather_data=weather_data, history=history, options=us_regions)


def get_weather(city, region):
    weather_data_json = {}
    try:
        weather_geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city},{region}&appid={api_key}"
        response_geo = requests.get(weather_geo_url)
        geo_data_response = response_geo.json()

        lat = geo_data_response[0]['lat']
        lon = geo_data_response[0]['lon']
    
        weather_data_url = f"https://api.openweathermap.org/data//2.5/forecast?units=imperial&lat={lat}&lon={lon}&appid={api_key}"
        response_weather = requests.get(weather_data_url)
        weather_data_response = response_weather.json()
        for i in range(6):
            jd = i * 8
            if jd == 40:
                jd -= 1
            date = datetime.utcfromtimestamp(weather_data_response["list"][jd]["dt"])
            formatted_date = date.strftime("%m/%d/%Y")
            weather_data_json.update({
            f"city{i}": geo_data_response[0]["name"],
            f"date{i}" : formatted_date,
            f"temperature{i}": f'Temp {weather_data_response["list"][jd]["main"]["temp"]}℉',
            f"wind{i}": f'Wind {weather_data_response["list"][jd]["wind"]["speed"]} MPH',
            f"humid{i}": f'Humidity {weather_data_response["list"][jd]["main"]["humidity"]}',
            f"icon{i}": f'https://openweathermap.org/img/w/{weather_data_response["list"][jd]["weather"][0]["icon"]}.png'
            })
    except:
        error_image = '/static/images/error_image.png'
        for i in range(6):
            jd = i * 8
            if jd == 40:
                jd -= 1
            weather_data_json.update({
                f"city{i}": f'Request Error {response_geo}',
                f"date{i}" : f'Request Error {response_geo}',
                f"temperature{i}": f'Request Error {response_geo}',
                f"wind{i}": f'Request Error {response_geo}',
                f"humid{i}": f'Request Error {response_geo}',
                f"icon{i}": error_image
            })
    return weather_data_json

def update_session_variables(city, region):
    counter = str(session['counter'])

    history = session['history']
    history[counter].update({'visibility': 'visible', 'city': city, 'region': region})

    counter = int(counter)
    counter += 1
    session['counter'] += 1
    if counter > 4:
        counter = 0
        session['counter'] = 0
    


if __name__ == "__main__":
    app.run(port=8000, debug=True)
import requests
from datetime import datetime

def get_wind_direction(degrees):
    if 337.5 <= degrees <= 22.5:
        return "Northern"
    elif 22.5 < degrees <= 67.5:
        return "Northeastern"
    elif 67.5 < degrees <= 112.5:
        return "East"
    elif 112.5 < degrees <= 157.5:
        return "Southeastern"
    elif 157.5 < degrees <= 202.5:
        return "Southern"
    elif 202.5 < degrees <= 247.5:
        return "Southwestern"
    elif 247.5 < degrees <= 292.5:
        return "West"
    else:
        return "Northwestern"

def get_weather(city):
    api_key = "981a0143485f2a3771ac178270480c46"  #  Key API OpenWeatherMap

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'message' in data:
            return None
        else:
            weather_data = {
                "time": datetime.fromtimestamp(data["dt"]),
                "title": data["weather"][0]["description"],
                "temperature": round(data["main"]["temp"]),
                "humidity": round(data["main"]["humidity"]),
                "wind_speed": round(data["wind"]["speed"]),
                "wind_dir": get_wind_direction(data["wind"]["deg"])
            }
            return weather_data
            
    else:
        return None

def get_city_from_user():
    city = input("Enter city name (press Enter to use Kyiv): ")
    if not city:  # If the user pressed Enter, we leave the city of Kyiv as the default
        city = "Kyiv"
    return city
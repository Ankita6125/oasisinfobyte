import requests
from django.shortcuts import render
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
print("Loaded API_KEY:", API_KEY)

def index(request):
    weather = None
    forecast = []
    selected_unit = "metric"  

    if request.method == "POST":
        city = request.POST.get("city")
        selected_unit = request.POST.get("unit", "metric")  
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={selected_unit}"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={selected_unit}"

        try:
            weather_response = requests.get(weather_url)
            forecast_response = requests.get(forecast_url)
            data = weather_response.json()
            forecast_data = forecast_response.json()

            if data["cod"] == 200 and forecast_data["cod"] == "200":
                icon_code = data["weather"][0]["icon"]
                icon_class = map_icon_to_fa(icon_code)

                weather = {
                    "city": city.title(),
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "icon": icon_class
                }

                forecast = [
                    {
                        "date": item["dt_txt"].split(" ")[0],
                        "temp": item["main"]["temp"]
                    }
                    for i, item in enumerate(forecast_data["list"]) if i % 8 == 0
                ]
            else:
                weather = None

        except Exception as e:
            print("Error:", e)
            weather = None
            forecast = []

    return render(request, "weather/index.html", {
        "weather": weather,
        "forecast": forecast,
        "selected_unit": selected_unit  
    })

def map_icon_to_fa(icon_code):
    code = icon_code[:2]
    mapping = {
        "01": "fa-sun",
        "02": "fa-cloud-sun",
        "03": "fa-cloud",
        "04": "fa-cloud-meatball",
        "09": "fa-cloud-showers-heavy",
        "10": "fa-cloud-sun-rain",
        "11": "fa-bolt",
        "13": "fa-snowflake",
        "50": "fa-smog",
    }
    return mapping.get(code, "fa-cloud")

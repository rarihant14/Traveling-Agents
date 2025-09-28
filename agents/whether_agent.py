import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_forecast(city: str, start_date, end_date):
    """
    Fetch 5-day weather forecast for the city using OpenWeather API.
    Returns list of dicts: {date, temp, description}.
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        forecasts = []
        if "list" in data:
            for entry in data["list"]:
                dt_txt = entry["dt_txt"].split(" ")[0]
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]
                forecasts.append({
                    "date": dt_txt,
                    "temp": temp,
                    "description": desc
                })

        # filter by trip dates
        forecasts = [f for f in forecasts if start_date <= f["date"] <= end_date]
        return forecasts
    except Exception as e:
        return [{"date": "N/A", "temp": "N/A", "description": str(e)}]

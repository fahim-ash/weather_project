import json
import requests
from datetime import datetime

class BdDistrictServie:

    def get_district(self):
        with open('bd_districts.json', 'r', encoding='utf-8') as file:
            districts = json.load(file)
            return districts.get("districts")

    def get_url(self, lat, long):
        return f'https://api.open-meteo.com/v1/forecast'


class WeatherService:
    def __init__(self):
        self.district_service = BdDistrictServie()
        self.district_list = self.district_service.get_district() 

    def fetch_weather(self, lat, long):
        API_URL = self.district_service.get_url(lat, long)
        params = {
            "latitude": lat,
            "longitude": long,
            "hourly": "temperature_2m",
            "timezone": "auto",
            "forecast_days": 7
        }
        response = requests.get(API_URL, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None

    def calculate_average(self, weather_data):
        hourly_temps = weather_data["hourly"]["temperature_2m"]
        two_pm_temps = hourly_temps[14::24]
        return sum(two_pm_temps) / len(two_pm_temps)

    def get_coolest_districts(self):
        district_temps = []
        for district in self.district_list:
            res = self.fetch_weather(district["lat"], district["long"])
            if res:
                avg_temp = self.calculate_average(res)
                district_temps.append({"district": district["name"], "avg_temp": avg_temp})

        district_temps.sort(key=lambda x: x["avg_temp"])
        return district_temps[:10]
#!/usr/bin/env python3

import json
import requests
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ICON_MAP = {
    "01d": "☀️",
    "02d": "⛅️",
    "03d": "☁️",
    "04d": "☁️",
    "09d": "🌧️",
    "10d": "🌦️",
    "11d": "⛈️",
    "13d": "🌨️",
    "50d": "🌫",
}

UNITS_MAP = {
    "standard": ("K", "m/sec"),
    "metric": ("°C","m/sec"),
    "imperial": ("°F", "mph"),
}

COMPASS_POINTS = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW', 'N']
def deg_to_dir(deg):
    deg = deg%360
    for i in range(len(COMPASS_POINTS)):
        d = i*22.5
        if d-11.25 <= deg and deg < d+11.25:
           return COMPASS_POINTS[i]

    return 'Uknown'

def main():
    apikey = os.getenv("WAYBAR_WEATHER_APIKEY")
    lat = os.getenv("WAYBAR_WEATHER_LAT", "52.52")
    lon = os.getenv("WAYBAR_WEATHER_LON", "13.38")
    units = os.getenv("WAYBAR_WEATHER_UNITS", "metric")
    exclude = os.getenv("WAYBAR_WEATHER_EXCLUDE", "minutely,hourly,daily")

    data = {}
    try:
        url = (f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}"
               f"&lon={lon}&units={units}&exclude={exclude}&appid={apikey}")
        weather = requests.get(url).json()

    except Exception as e:
        return print({})

    if weather.get("cod"):
        data["text"] = "[weather] Error {}: {}".format(
            weather.get("cod"), weather.get("message")
        )
        data["class"] = "weather"
        print(json.dumps(data))
        # sys.exit(data["text"])
        sys.exit()

    temp = weather["current"]["temp"]
    icon = ICON_MAP.get(weather["current"]["weather"][0]["icon"], "")
    feels_like = weather["current"]["feels_like"]
    humidity = weather["current"]["humidity"]
    pressure = weather["current"]["pressure"]
    sunrise = datetime.fromtimestamp(
        weather["current"]["sunrise"], ZoneInfo(weather["timezone"])
    ).strftime("%H:%M")
    sunset = datetime.fromtimestamp(
        weather["current"]["sunset"], ZoneInfo(weather["timezone"])
    ).strftime("%H:%M")
    wind_speed = weather["current"]["wind_speed"]
    wind_direction = deg_to_dir(weather["current"]["wind_deg"])
    uvi = weather["current"]["uvi"]

    data["text"] = f"{icon} {temp:.1f}{UNITS_MAP[units][0]}"
    data["tooltip"] = f"""Feels like: {feels_like:.1f}{UNITS_MAP[units][0]}
Pressure: {pressure} hPa
Humidity: {humidity}%
UV Index: {uvi}
Sunrise: {sunrise}
Sunset: {sunset}
Wind: {wind_direction}, {wind_speed:.0f} {UNITS_MAP[units][1]}"""
    if "daily" in weather:
        temp_min = weather["daily"][0]["temp"]["min"]
        temp_max = weather["daily"][0]["temp"]["max"]
        data["tooltip"] = f"""Min: {temp_min:.1f}{UNITS_MAP[units][0]}
Max: {temp_max:.1f}{UNITS_MAP[units][0]}
""" + data["tooltip"]

    data["class"] = "weather"

    print(json.dumps(data))


if __name__ == "__main__":
    main()

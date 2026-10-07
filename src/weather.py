from dataclasses import dataclass
from pathlib import Path
import json
import urllib.request
from collections import defaultdict

CITIES_FILE = "Cities.txt"
API_TEMPLATE = "https://wttr.in/{City}?format=j1"

GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

@dataclass
class WeatherData:
    city: str
    temperature: int
    country: str

def load_cities(path):
    cites = []

    with open(path, encoding="utf-8") as file:
        for line in file:
            name = line.strip()

            if name == "":
                continue

            if name not in cites:
                cites.append(name)

    return cites

def fetch_weather(city):
    url = API_TEMPLATE.replace("{City}", city)
    print(f"{GREEN}Запрос:{RESET}", url)

    with urllib.request.urlopen(url) as response:
        text = response.read().decode("utf-8")

    data = json.loads(text)

    temp_c = int(data["current_condition"][0]["temp_C"])
    country = data["nearest_area"][0]["country"][0]["value"]

    weather = WeatherData(
        city=city,
        temperature=temp_c,
        country=country,
    )

    return weather

def group_by_country(weathers):
    groups = defaultdict(list)

    for weather in weathers:
        groups[weather.country].append(weather)

    return groups
    
def main():
    cities = load_cities(CITIES_FILE)
    weathers = []

    for city in cities:
        weather = fetch_weather(city)
        weathers.append(weather)

    print()
    print(f"{BLUE}Погода по городам:{RESET}")
    for weather in weathers:
        print(f"{weather.city}, {weather.country} {weather.temperature:+d} °C")

    groups = group_by_country(weathers)

    print()
    print(f"{RED}Статистика по странам:{RESET}")
    for counrty, cites_in_country in groups.items():
        count = len(cites_in_country)

        temperatures = []
        for w in cites_in_country:
            temperatures.append(w.temperature)

        avg = sum(temperatures) / len(temperatures)
        minimum = min(temperatures)
        maximum = max(temperatures)

        print(f"{counrty} - {count} cities, avg: {round(avg):+d} °C, min: {minimum:+d} °C, max: {maximum:+d} °C")

if __name__ == "__main__":
    main()
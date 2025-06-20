import requests
import json
from datetime import datetime

def get_temperature(city):
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': '441f54eb9b8819b3a05d1674294bb055', 'units': 'metric'}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data['main']['temp']
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def save_weather_report(city, filename="weather_log.json"):
    """Récupère la météo et la sauvegarde dans un fichier JSON"""

    temp = get_temperature(city)
    if temp is None:
        return False

    report = {
        'city': city,
        'temperature': temp,
        'timestamp': datetime.now().isoformat()
    }

    try:
        with open(filename, 'r') as f:
            reports = json.load(f)
    except FileNotFoundError:
        reports = []

    reports.append(report)

    with open(filename, 'w') as f:
        json.dump(reports, f)

    return True
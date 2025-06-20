import requests

def get_temperature(city):
    """Récupère la température d'une ville via une API"""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': '441f54eb9b8819b3a05d1674294bb055',  # Clé bidon pour ce TP
        'units': 'metric'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['main']['temp']
    else:
        return None

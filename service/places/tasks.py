import datetime

import requests
from celery import shared_task

from .models import Place, Whether


OPEN_WEATHER_API = '703b9f29de5b07846229126df922601e'


@shared_task
def get_weather_report():
    places = Place.objects.all()

    for place in places:
        res = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={'lat': place.lat,
                    'lon': place.lon,
                    'units': 'metric',
                    'lang': 'ru',
                    'APPID': OPEN_WEATHER_API}
            )
        data = res.json()

        whether, created = Whether.objects.update_or_create(
            place=place,
            defaults={
                'atmosphere_pressure': data['main']['pressure'],
                'air_humidity': data['main']['humidity'],
                'direction_wind': data['wind']['deg'],
                'wind_speed': data['wind']['speed'],
                'temperature': data['main']['temp'],
                'date': datetime.datetime.now(),
            },
        )

        if created:
            print(f"create object: {whether}")
        else:
            print(f"update object: {whether}")

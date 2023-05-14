import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Place, Whether
import requests

OPEN_WEATHER_API = '703b9f29de5b07846229126df922601e'


@receiver(post_save, sender=Place)
def update_weather(sender, instance: Place, **kwargs):

    res = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={'lat': instance.lat,
                'lon': instance.lon,
                'units': 'metric',
                'lang': 'ru',
                'APPID': OPEN_WEATHER_API}
    )
    data = res.json()

    whether, created = Whether.objects.update_or_create(
        place=instance,
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

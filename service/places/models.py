import datetime
import requests
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django_admin_geomap import GeoItem
from django.db import models


class Place(models.Model, GeoItem):
    """
    Модель 'Примечательные места'
    name: Название
    rate: Рейтинг от 1 до 25
    lat: широта
    lon: долгота
    """
    name = models.CharField(max_length=100)
    rate = models.IntegerField(default=1, validators=[MaxValueValidator(25), MinValueValidator(1)])
    lat = models.FloatField(null=True, blank=True, validators=[MaxValueValidator(90), MinValueValidator(-90)])
    lon = models.FloatField(null=True, blank=True, validators=[MaxValueValidator(180), MinValueValidator(-180)])

    def update_or_create_weather(self) -> None:

        res = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={'lat': self.lat,
                    'lon': self.lon,
                    'units': 'metric',
                    'lang': 'ru',
                    'APPID': settings.WEATHER_KEY_API}
        )
        data = res.json()

        whether, created = Whether.objects.update_or_create(
            place=self,
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

    @property
    def geomap_popup_view(self):
        return "<strong>{}</strong>".format(str(self))

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view

    @property
    def geomap_popup_common(self):
        return self.geomap_popup_view

    @property
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property
    def geomap_latitude(self):
        return '' if self.lat is None else str(self.lat)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Примечательное место'
        verbose_name_plural = 'Примечательные места'
        constraints = [
            models.CheckConstraint(
                check=models.Q(rate__gte=1) & models.Q(rate__lte=25),
                name="rate range",
            ),
            models.CheckConstraint(
                check=models.Q(lon__gte=-180.0) & models.Q(lon__lte=180.0),
                name='longitude range'
            ),
            models.CheckConstraint(
                check=models.Q(lat__gte=-90.0) & models.Q(lat__lte=90.0),
                name='latitude range'
            ),
        ]


class Whether(models.Model):
    """Модель 'Сводка погоды'
    atmosphere_pressure: атмосферное давление
    air_humidity: влажность воздуха в %
    direction_wind: направление ветра
    wind_speed: скорость ветра
    temperature: температура
    place: место
    """

    atmosphere_pressure = models.FloatField(verbose_name='Атмосферное давление')
    air_humidity = models.FloatField(verbose_name='Влажность воздуха')
    direction_wind = models.FloatField(verbose_name='Направление ветра')
    wind_speed = models.FloatField(verbose_name='Скорость ветра')
    temperature = models.FloatField(verbose_name='Температура')
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        verbose_name='Примечательное место',
    )
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата')

    def __str__(self):
        return self.place.name

    class Meta:
        verbose_name = 'Погода'
        verbose_name_plural = 'Погода'
        constraints = [
            models.CheckConstraint(
                check=models.Q(air_humidity__gte=0) & models.Q(air_humidity__lte=100),
                name="air humidity",
            ),
            models.CheckConstraint(
                check=models.Q(direction_wind__gte=0) & models.Q(direction_wind__lte=360),
                name="direction wind",
            ),
        ]

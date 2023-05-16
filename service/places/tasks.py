from celery import shared_task
from .models import Place


@shared_task
def get_weather_report():
    places = Place.objects.all()

    for place in places:
        place.update_or_create_weather()

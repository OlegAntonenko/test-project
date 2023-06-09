import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

from celery.schedules import crontab
from celery import Celery

app = Celery('service')
app.config_from_object('django.conf:settings', namespace="CELERY")

app.conf.beat_schedule = {
    'send_email_users': {
        'task': 'news.tasks.send_email_users',
        'schedule': crontab(hour=12, minute=0),
    },
    'get_weather_report': {
            'task': 'places.tasks.get_weather_report',
            'schedule': crontab(minute='0', hour='*/1'),
        },
}

app.autodiscover_tasks()

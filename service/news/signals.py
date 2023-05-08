from constance.signals import config_updated
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    # Не получилось вызвать constance_updated после обновления настроек TEXT, TITLE, SEND_TIME.
    minute_old = ''
    hour_old = ''
    minute = ''
    hour = ''
    try:
        schedule = CrontabSchedule.objects.get(minute=minute_old, hour=hour_old, timezone='Asia/Krasnoyarsk')
        schedule.hour = hour
        schedule.minute = minute
        schedule.save()
    except ObjectDoesNotExist:
        print('Not match object')
    print(sender, key, old_value, new_value)

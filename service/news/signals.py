from constance.signals import config_updated
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):

    if key == 'TIME_SEND':
        try:
            task = PeriodicTask.objects.get(name='send_email_users')
            task.crontab.hour = new_value.hour
            task.crontab.minute = new_value.minute
            task.crontab.save()
        except ObjectDoesNotExist:
            print('Not match object')

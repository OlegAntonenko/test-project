from .models import Place
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Place)
def update_weather(sender, instance: Place, **kwargs):
    instance.update_or_create_weather()

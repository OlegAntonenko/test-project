import datetime

from celery import shared_task
from news.models import News
from constance import config
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.html import strip_tags


@shared_task
def send_email_users() -> None:
    """Send messages to email users"""
    today = datetime.datetime.today()
    news = News.objects.filter(date__date=today)
    users = User.objects.all()
    email_list = [user.email for user in users]

    if news:
        message = config.TEXT
        for n in news:
            message += '\n\n' + n.title + '\n' + strip_tags(n.text)
    else:
        message = 'No news'

    send_mail(
        subject=config.TITLE,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
    )

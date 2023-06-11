from celery import shared_task
import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import News, Subscribers


def send_notifications_every_monday(news, subscribers):
    for sub in subscribers:
        html_content = render_to_string(
            'email/daily_news.html',
            {
                'link': settings.SITE_URL,
                'news': news,
                'user': sub[0]
            }
        )

        msg = EmailMultiAlternatives(
            subject='Daily news',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub[1]],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_notify_every_monday_8am():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    news = News.objects.filter(date_in__gte=last_week)
    subscribers = Subscribers.objects.all().values_list('user__username', 'user__email')
    send_notifications_every_monday(news, subscribers)

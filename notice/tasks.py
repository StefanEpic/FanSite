from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def send_notify_about_message(message, text):
    html_content = render_to_string(
        'email/message_email.html',
        {
            'user': message.author,
            'author': message.notice.author,
            'text': text[0],
            'title': message.notice.title,
            'smile': text[1],
        }
    )

    msg = EmailMultiAlternatives(
        subject=message.notice.title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[message.author.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_notify_about_notice(message, text):
    html_content = render_to_string(
        'email/message_email.html',
        {
            'user': message.notice.author,
            'author': message.author,
            'text': text[0],
            'title': message.notice.title,
            'smile': text[1],
        }
    )

    msg = EmailMultiAlternatives(
        subject=message.notice.title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[message.notice.author.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

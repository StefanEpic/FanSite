from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def send_notify_about_message(title, user, email_text):
    html_content = render_to_string(
        'email/message_email.html',
        {
            'user': user,
            'message': email_text,
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body=email_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save

from .models import Message, Notice
from .tasks import send_notify_about_message


@receiver(pre_delete, sender=Message)
def notify_about_delete_message(sender, instance, **kwargs):
    message = instance
    title = message.notice.title
    user = message.author
    email_text = f'<h2>Hello, {user}!</h2><h3>{message.notice.author} rejected your response to the ad "{title}"! :(</h3>'
    send_notify_about_message(title, user, email_text)


@receiver(pre_save, sender=Message)
def notify_about_apply_message(sender, instance, **kwargs):
    message = instance
    title = message.notice.title
    user = message.author
    email_text = f'<h2>Hello, {user}!</h2><h3>{message.notice.author} accepted your response to the ad "{title}"! :)</h3>'
    send_notify_about_message(title, user, email_text)

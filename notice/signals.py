from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from .models import Message
from .tasks import send_notify_about_message


@receiver(post_delete, sender=Message)
def notify_about_delete_message(sender, instance, **kwargs):
    message = instance
    text = ['rejected your response to the ad', ':(']
    send_notify_about_message(message, text)


@receiver(post_save, sender=Message)
def notify_about_apply_message(sender, instance, **kwargs):
    message = instance
    text = ['accepted your response to the ad', ':)']
    send_notify_about_message(message, text)

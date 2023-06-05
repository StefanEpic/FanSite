from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Message
# from .tasks import send_notify_about_message


@receiver(post_delete, sender=Message)
def notify_about_task(**kwargs):
    message = kwargs['instance']

    # send_notify_about_message(task, label)

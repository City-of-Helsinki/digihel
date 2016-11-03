from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Feedback
from .tasks import notify_new_feedback


@receiver(post_save, sender=Feedback, dispatch_uid='send_feedback_notification')
def send_feedback_notification(sender, instance, **kwargs):
    notify_new_feedback.delay(instance.id)

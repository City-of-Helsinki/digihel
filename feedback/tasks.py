from celery import shared_task

from .models import Feedback


@shared_task
def notify_new_feedback(feedback_id):
    obj = Feedback.objects.get(id=feedback_id)
    obj.notify()

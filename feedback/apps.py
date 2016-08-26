from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    name = 'feedback'

    def ready(self):
        from .signals import send_feedback_notification

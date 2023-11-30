from django.apps import AppConfig


class DistributionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'distribution'

    def ready(self):
        from django.db.models.signals import post_save
        from distribution.models import Mailing
        from distribution.signals import create_message

        post_save.connect(create_message, sender=Mailing, dispatch_uid="create_message")

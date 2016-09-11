from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reporte


@receiver(post_save, sender=Reporte)
def send_report_email(sender, instance, created, **kwars):
    pass

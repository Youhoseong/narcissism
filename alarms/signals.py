from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from . import models

@receiver(post_save, sender=models.Alarm)
def Alarm_post_save(sender, **kwargs):
    print("new msg")
    """messages.info(request, "You've got new mail")"""
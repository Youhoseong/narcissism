from django.db import models
from core import models as core_model
from users import models as user_model

class Alarm(core_model.TimeStampedModel):
    sender = models.ForeignKey(user_model.User, related_name="alarm_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(user_model.User, related_name="alarm_receiver", on_delete=models.CASCADE)
    title = models.CharField(max_length = 40, blank=False, null=True)
    content = models.TextField(blank=True)
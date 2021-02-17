from django.db import models
from core import models as core_models
from purchases import models as purchase_models
from users import models as user_models
# Create your models here.


class Comment(core_models.TimeStampedModel):
    context = models.CharField(max_length=150, blank=False, default=" ")
    purchase = models.ForeignKey(purchase_models.Purchase, related_name="comment", on_delete=models.CASCADE)
    
    writer = models.ForeignKey(user_models.User, related_name="comment", on_delete=models.CASCADE)
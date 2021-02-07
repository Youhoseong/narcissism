from django.db import models
from core import models as core_models

class List(core_models.TimeStampedModel):

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    purchases = models.ManyToManyField("purchases.Purchase", blank=True)


    def __str__(self):
        return self.name
    
    def count_purchases(self):
        return self.purchases.count()
    count_purchases.short_description = "Number of Purchases"
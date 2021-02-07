from django.db import models
from core import models as core_models

class Review(core_models.TimeStampedModel):

    review = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    purchases = models.ManyToManyField("purchases.Purchase", blank=True)
    rate = models.IntegerField()

    def __str__(self):
        return self.review

    def rating(self):
        return self.rate
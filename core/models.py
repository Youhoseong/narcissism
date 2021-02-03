from django.db import models


# Create your models here.

class TimeStampedModel(models.Model):

    """ Time Stamp Model Definition """

    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True
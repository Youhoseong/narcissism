from django.contrib import admin
from . import models

@admin.register(models.Alarm)
class ListAdmin(admin.ModelAdmin):

    list_display=(
        "sender",
        "receiver",
        "content",
        "created",
        "category",
        "ischeck",
        "isFirst",
    )

    search_fields = ("sender",)
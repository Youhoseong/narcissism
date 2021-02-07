from django.contrib import admin
from . import models

@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    list_display=(
        "name",
        "user",
        "count_purchases",
    )

    search_fields = ("name",)

    filter_horizontal = ("purchases",)

from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    fieldsets = (("Custom Profile", {"fields": ("title","host", "closed")}),)

    
    list_display = (
       "title",
       "host",
       "closed",
    )
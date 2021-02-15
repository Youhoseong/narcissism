from django.contrib import admin
from . import models
# Register your models here.

class PhotoInline(admin.TabularInline):

    model = models.Photo

@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
   pass


@admin.register(models.Material)
class MaterialPurchaseAdmin(admin.ModelAdmin):
   
   inlines = (PhotoInline,)

   fieldsets = (("Custom Profile", {
      "fields": (
         "closed", "title", "category","host", "explain", "price", "max_people", "participants", "unit", "total", "link_address"
      )}),)

   list_display = (
      "closed",
      "title",
      "category",
      "host",
      "max_people",
      "price",
      "total",
      "unit",
      "amount_per_person",
      "price_per_person",
      "pk",
   )

   filter_horizontal = (
      "participants",
   )

@admin.register(models.Immaterial)
class ImmaterialPurchaseAdmin(admin.ModelAdmin):
   
   inlines = (PhotoInline,)

   fieldsets = (("Custom Profile", {"fields": ("closed", "title", "category", "host", "explain", "price", "max_people", "participants", )}),)

   list_display = (
      "closed",
      "title",
      "category",
      "host",
      "max_people",
      "price",
      "price_per_person",
      "pk"
   )

   filter_horizontal = (
      "participants",
   )
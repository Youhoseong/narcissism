from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
   fieldsets = (("comment field", {"fields": ("context", "purchase", "writer")}),)

   list_display = (
       "context",
       "purchase",
       "writer"
   )

 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + \
        (("Custom Profile", {"fields": ("avatar", "gender", "bio",
                                        "birthdate", "address", "login_method")}),)

    
    list_display = (
        "username",
        "gender",
        "first_name",
        "last_name",
        "address",
        "email",
        "email_verified",
        "login_method"
    )
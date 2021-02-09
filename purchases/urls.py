
from django.contrib import admin
from django.urls import path
from . import views

app_name = "purchases"
urlpatterns = [
    # user pk 추가해야함 => login 구현 후
    path("create/", views.create_user_location, name="location_create")
]

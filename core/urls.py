from django.contrib import admin
from django.urls import path, include
from purchases import views as purchase_views

app_name = "core"

urlpatterns = [path("", purchase_views.HomeView.as_view(), name="home")]


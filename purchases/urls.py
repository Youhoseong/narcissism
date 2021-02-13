from django.contrib import admin
from django.urls import path
from . import views

app_name = "purchases"
urlpatterns = [path("<int:pk>/", views.PurchaseDetailView.as_view(), name="purchase")]

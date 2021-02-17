from django.contrib import admin
from django.urls import path
from . import views

app_name = "purchases"
urlpatterns = [
    path("<int:pk>/", views.PurchaseDetailView.as_view(), name="purchase"),
    path("select/", views.PurchaseSelectView.as_view(), name="select"),
    path("create_m/", views.CreateMaterialView.as_view(), name="create_m"),
    path("create_i/", views.CreateImmaterialView.as_view(), name="create_i"),
]

from django.contrib import admin
from django.urls import path
from . import views

app_name = "alarms"
urlpatterns = [
    path("", views.AlarmView.as_view(), name="alarm_list"),
    path("<int:pk>/", views.AlarmDetailView.as_view(), name="alarm_detail"),
    path("message/<int:receiver_pk>/", views.MessageView.as_view(), name="message"),
    path("check/<int:pk>", views.alarmcheckview, name="check")
]
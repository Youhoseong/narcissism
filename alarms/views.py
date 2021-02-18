from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.urls import reverse_lazy
from . import models, forms

# Create your views here.

class AlarmView(ListView):
    model = models.Alarm
    template_name = "alarms/alarm_list"
    context_object_name = "alarms"
    ordering = "-created"

class AlarmDetailView(DetailView):
    model = models.Alarm
    template_name = "alarms/alarm_detail.html"

class MessageView(FormView):
    template_name = "alarms/write_msg.html"
    form_class = forms.MessageForm
    success_url = reverse_lazy("core:home")

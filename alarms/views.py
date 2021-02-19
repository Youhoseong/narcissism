from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.urls import reverse_lazy
from . import models, forms
from purchases import models as purchase_model
from django.contrib import messages

# Create your views here.

class AlarmView(ListView):
    model = models.Alarm
    template_name = "alarms/alarm_list.html"
    context_object_name = "alarms"
    ordering = "-created"

class AlarmDetailView(DetailView):
    model = models.Alarm
    template_name = "alarms/alarm_detail.html"

class MessageView(FormView):
    template_name = "alarms/write_msg.html"
    form_class = forms.MessageForm

    def form_valid(self, form):
        new_message = form.save()
        """form.save_m2m()"""
        new_message.save()
        messages.success(self.request, "메시지를 전송했습니다.")
        return redirect(reverse("alarms:alarm_list"))

def participant_full(request, purchase_model):
    print("넘어왓으")
    sender = purchase_model.host
    receiver = purchase_model.host
    title = purchase_model.title + " 가 마감되었습니다."
    content = "공동구매가 마감되었습니다."

    print(sender, receiver, title, content)

    msg = models.Alarm.objects.create(
        sender = sender,
        receiver = receiver,
        title = title,
        content = content,
    )
    msg.save()
from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.urls import reverse_lazy
from . import models, forms
from users import models as user_models
from purchases import models as purchase_model
from django.contrib import messages
from users import mixins
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

class AlarmView(mixins.LoggedInOnlyView, ListView):
    model = models.Alarm
    template_name = "alarms/alarm_list.html"
    context_object_name = "alarms"
    ordering = "-created"

def alarmcheckview(request, pk):
    if request.method == 'GET':
        alarm = models.Alarm.objects.get(pk=pk)
        alarm.ischeck=True
        alarm.save()
        return redirect(reverse("alarms:alarm_list"))

class AlarmDetailView(mixins.LoggedInOnlyView, DetailView):
    model = models.Alarm
    template_name = "alarms/alarm_detail.html"

class MessageView(mixins.LoggedInOnlyView, FormView):
    template_name = "alarms/write_msg.html"
    form_class = forms.MessageForm

    def form_valid(self, form):
        new_message = form.save()
        """form.save_m2m()"""
        new_message.sender = self.request.user
        receiver_pk = self.kwargs['receiver_pk']
        receiver_model = user_models.User.objects.get(pk=receiver_pk)
        new_message.receiver = receiver_model
        sender = new_message.sender
        receiver = new_message.receiver

        model_check1 = models.Alarm.objects.filter(sender = sender, receiver = receiver)
        model_check2 = models.Alarm.objects.filter(sender = receiver, receiver = sender)

        model_check = (model_check1 | model_check2)

        if model_check.exists():
            new_message.isFirst = False
            print(new_message.isFirst)
        else:
            new_message.isFirst = True
            print(new_message.isFirst)

        new_message.category = "dm"
        
        new_message.save()
        messages.success(self.request, "메시지를 전송했습니다.")
        return redirect(reverse("alarms:alarm_list"))



def participant_full(request, purchase_model):
    sender = purchase_model.host
    receiver = purchase_model.host
    title = purchase_model.title + " 가 마감되었습니다."
    content = "공동구매 인원이 충족되었습니다."

    print(sender, receiver, title, content)

    msg = models.Alarm.objects.create(
        sender = sender,
        receiver = receiver,
        title = title,
        content = content,
    )
    msg.save()
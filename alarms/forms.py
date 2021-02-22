from django import forms
from . import models as alarm_model


class MessageForm(forms.ModelForm):
    class Meta:
        model = alarm_model.Alarm
        fields = (
            "receiver",
            "title",
            "content",
        )

    def save(self, *args, **kwargs):
        message = super().save(commit=False)
        return message
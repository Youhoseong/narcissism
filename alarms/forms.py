from django import forms
from users import models as user_model
from . import models as alarm_model


class MessageForm(forms.ModelForm):
    class Meta:
        model = alarm_model.Alarm
        fields = (
            "sender",
            "receiver",
            "title",
            "content",
        )
        widgets = {
            "sender": forms.TextInput(attrs={"placeholder": "Sender"}),
            "receiver": forms.TextInput(attrs={"placeholder": "Receiver"}),
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "content": forms.EmailInput(attrs={"placeholder": "Content"}),
        }
    
    """def save(self, *args, **kwargs):
        msg = super().save(commit=False)
        sender = self.cleaned_data.get("sender")
        try:
            user_model.User.objects.get(username=sender)
            
        except user_model.User.DoesNotExist:
            return username
            
        receiver = self.cleaned_data.get("receiver")
        try:
            models.User.objects.get(username=username)
            raise forms.ValidationError(
                "That username is already taken", code="existing_username"
            )
        except models.User.DoesNotExist:
            return username
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")
        msg.save()"""
from . import models
from django import forms


class CommentForm(forms.Form):
 
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "댓글을 입력하세요."})
    )

    def clean_comment(self):
        data = self.cleaned_data['comment']

        return data
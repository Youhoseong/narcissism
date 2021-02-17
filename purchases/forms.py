from . import models
from django import forms


class CreateMaterialForm(forms.Form):

    title = forms.CharField(initial="제목을 작성해주세요")
    category = forms.ChoiceField(choices=models.Material.category_choice, required=True)
    closed = forms.DateTimeField()
    max_people = forms.IntegerField()
    price = forms.IntegerField()
    total = forms.IntegerField()
    unit = forms.CharField()
    explain = forms.CharField(widget=forms.Textarea)
    link_address = forms.URLField()
    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )


class CreateImmaterialForm(forms.ModelForm):
    class Meta:
        model = models.Immaterial
        fields = ("title", "closed", "explain", "category", "max_people", "price")
        widgets = {"explain": forms.Textarea(attrs={"col": 40, "row": 30})}

    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )
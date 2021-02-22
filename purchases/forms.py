from . import models
from django import forms


class CreateMaterialForm(forms.Form):

    title = forms.CharField(label= "제목")
    category = forms.ChoiceField(choices=models.Material.category_choice, required=True, label="카테고리")
    closed = forms.DateTimeField(widget=forms.DateInput(attrs={"class": "datepicker"}), label="마감 일자")
    max_people = forms.IntegerField(label="공동구매 모집 인원")
    price = forms.IntegerField(label="상품 가격")
    unit = forms.CharField(label="상품 양(ex. 2kg, 3개..)")
    explain = forms.CharField(widget=forms.Textarea, label="본문")
    link_address = forms.URLField(label="상품 판매 홈페이지 주소")
    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False, label="상품 사진"
    )


class CreateImmaterialForm(forms.ModelForm):
    class Meta:
        model = models.Immaterial
        fields = ("title", "closed", "explain", "category", "max_people", "price")
        widgets = {"explain": forms.Textarea(attrs={"col": 40, "row": 30}),}

    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )

    def save(self, *args, **kwargs):
        immaterial = super().save(commit=False)
        return immaterial


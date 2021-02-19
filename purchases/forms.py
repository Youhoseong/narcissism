from . import models
from django import forms


class CreateMaterialForm(forms.Form):

    title = forms.CharField(initial="제목을 작성해주세요")
    category = forms.ChoiceField(choices=models.Material.category_choice, required=True)
    closed = forms.DateTimeField(widget=forms.DateInput(attrs={"class": "datepicker"}))
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
        labels = {
            "title": "제목",
            "closed": "마감 일자",
            "explain": "본문",
            "category": "카테고리",
            "max_people": "공동구매 모집 인원",
            "price": "상품 가격",
        }

    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
        label="상품 사진",
    )

    def save(self, *args, **kwargs):
        immaterial = super().save(commit=False)
        return immaterial


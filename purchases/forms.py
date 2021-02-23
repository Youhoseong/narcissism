from django import forms
import datetime
from pytz import timezone
from . import models


class CreateMaterialForm(forms.Form):

    title = forms.CharField(label="제목")
    category = forms.ChoiceField(
        choices=models.Material.category_choice, required=True, label="카테고리"
    )
    closed = forms.DateTimeField(
        widget=forms.DateInput(attrs={"class": "datepicker"}), label="마감 일자"
    )
    max_people = forms.IntegerField(label="공동구매 모집 인원(본인 포함)")
    price = forms.IntegerField(label="상품 가격")
    unit = forms.CharField(label="상품 양(ex. 2kg, 3개..)")
    explain = forms.CharField(widget=forms.Textarea, label="본문")
    link_address = forms.URLField(label="상품 판매 홈페이지 주소")
    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
        label="상품 사진",
    )

    def clean_closed(self):
        closed = self.cleaned_data["closed"]
        today = datetime.datetime.now(timezone("Asia/Seoul"))
        # 비교를 위해 자료형 변경
        closed = closed.replace(tzinfo=timezone("Asia/Seoul"))

        if today > closed:
            raise forms.ValidationError("마감 일자를 확인해주세요")
        else:
            return self.cleaned_data.get("closed")


class CreateImmaterialForm(forms.ModelForm):
    class Meta:
        model = models.Immaterial
        fields = ("title", "closed", "category", "max_people", "price", "explain")
        widgets = {"explain": forms.Textarea(attrs={"col": 40, "row": 30})}
        labels = {
            "title": "제목",
            "closed": "마감 일자",
            "explain": "본문",
            "category": "카테고리",
            "max_people": "공동구매 모집 인원(본인 포함)",
            "price": "상품 가격",
        }

    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
        label="상품 사진",
    )

    def clean_closed(self):
        closed = self.cleaned_data["closed"]
        today = datetime.datetime.now(timezone("Asia/Seoul"))
        # 비교를 위해 자료형 변경
        closed = closed.replace(tzinfo=timezone("Asia/Seoul"))

        if today > closed:
            raise forms.ValidationError("마감 일자를 확인해주세요")
        else:
            return self.cleaned_data.get("closed")

    def save(self, *args, **kwargs):
        immaterial = super().save(commit=False)
        return immaterial


class EditMaterialForm(forms.ModelForm):
    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
        label="상품 사진",
    )

    class Meta:
        model = models.Material
        fields = (
            "photos",
            "title",
            "category",
            "closed",
            "max_people",
            "price",
            "unit",
            "explain",
            "link_address",
        )
        widgets = {"explain": forms.Textarea(attrs={"col": 40, "row": 30})}
        labels = {
            "title": "제목",
            "category": "카테고리",
            "closed": "마감 일자",
            "max_people": "공동구매 모집 인원",
            "price": "상품 가격",
            "unit": "상품 양(ex. 2kg, 3개..)",
            "explain": "본문",
            "link_address": "상품 판매 홈페이지 주소",
        }

    def clean_closed(self):
        closed = self.cleaned_data["closed"]
        today = datetime.datetime.now(timezone("Asia/Seoul"))
        # 비교를 위해 자료형 변경
        closed = closed.replace(tzinfo=timezone("Asia/Seoul"))

        if today > closed:
            raise forms.ValidationError("마감 일자를 확인해주세요")
        else:
            return self.cleaned_data.get("closed")

    def clean_max_people(self):
        participants_count = self.instance.participants.count()
        changed_max_people = self.cleaned_data.get("max_people")
        if participants_count > changed_max_people:
            raise forms.ValidationError("현재 참가한 인원 수 보다 큰 모집 인원을 입력해주세요")
        else:
            return self.cleaned_data.get("max_people")


class EditImaterialForm(forms.ModelForm):
    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
        label="상품 사진",
    )

    class Meta:
        model = models.Immaterial
        fields = (
            "photos",
            "title",
            "closed",
            "explain",
            "category",
            "max_people",
            "price",
        )
        widgets = {"explain": forms.Textarea(attrs={"col": 40, "row": 30})}
        labels = {
            "title": "제목",
            "closed": "마감 일자",
            "explain": "본문",
            "category": "카테고리",
            "max_people": "공동구매 모집 인원",
            "price": "상품 가격",
        }

    def clean_closed(self):
        closed = self.cleaned_data["closed"]
        today = datetime.datetime.now(timezone("Asia/Seoul"))
        # 비교를 위해 자료형 변경
        closed = closed.replace(tzinfo=timezone("Asia/Seoul"))

        if today > closed:
            raise forms.ValidationError("마감 일자를 확인해주세요")
        else:
            return self.cleaned_data.get("closed")

    def clean_max_people(self):
        participants_count = self.instance.participants.count()
        changed_max_people = self.cleaned_data.get("max_people")
        if participants_count > changed_max_people:
            raise forms.ValidationError("현재 참가한 인원 수 보다 큰 모집 인원을 입력해주세요")
        else:
            return self.cleaned_data.get("max_people")

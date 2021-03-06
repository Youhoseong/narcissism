from django.db import models
from core import models as core_model
from users import models as user_model
from django.shortcuts import reverse

# Create your models here.


class Photo(core_model.TimeStampedModel):
    file = models.FileField(upload_to="room_photos")
    purchases = models.ForeignKey(
        "Purchase", related_name="photos", on_delete=models.CASCADE
    )


class Purchase(core_model.TimeStampedModel):
    status_ongoing = "진행 중"
    status_recruite_end = "모집 완료"
    status_expired = "기간 만료"
    status_finished = "거래 완료"
    status_choices = (
        (status_ongoing, "진행 중"),
        (status_recruite_end, "모집 완료"),
        (status_expired, "기간 만료"),
        (status_finished, "거래 완료"),
    )
    closed = models.DateTimeField()
    title = models.CharField(max_length=40, blank=True)
    host = models.ForeignKey(
        user_model.User, related_name="purchase", on_delete=models.CASCADE
    )
    explain = models.TextField(blank=True)

    max_people = models.IntegerField(default=0)  # 참여 총 인원
    participants = models.ManyToManyField(
        user_model.User, related_name="participate", blank=True
    )
    price = models.IntegerField(default=0)  # 총 가격
    address = models.CharField(max_length=80, blank=True)  # 게시글 작성자 주소.
    status = models.CharField(
        choices=status_choices, default=status_ongoing, max_length=16, blank=False
    )

    def thumbnail(self):
        try:
            (thumbnail,) = self.photos.all()[:1]
            return thumbnail.file.url
        except ValueError:
            return None

    def ratio(self):
        count = self.participants.count()
        try:
            x = count / self.max_people
            return int(x * 100)
        except ZeroDivisionError:
            return 0

    def price_per_person(self):
        return int(self.price / self.max_people)

    def dong(self):
        return self.address.split()[-1]


class Material(Purchase):
    category_food = "음식"
    category_daily = "생필품"
    category_other = "기타"

    category_choice = (
        (category_food, "음식"),
        (category_daily, "생필품"),
        (category_other, "기타"),
    )

    unit = models.CharField(max_length=5, blank=True)  # 단위
    link_address = models.URLField(blank=True)
    category = models.CharField(
        choices=category_choice, max_length=20, blank=False, default=category_food
    )

    def get_absolute_url(self):
        return reverse("purchases:material", kwargs={"pk": self.pk})


class Immaterial(Purchase):  # 물건 구매가 아닌 활동을 위한 사람을 구하는 게시글.
    category_service = "인터넷 서비스 공유"
    category_education = "교육"
    category_hobby = "여가 활동"
    category_other = "기타"

    category_choice = (
        (category_service, "인터넷 서비스 공유"),
        (category_education, "교육"),
        (category_hobby, "여가 활동"),
        (category_other, "기타"),
    )

    category = models.CharField(
        choices=category_choice, max_length=20, blank=False, default=category_service
    )

    def get_absolute_url(self):
        return reverse("purchases:immaterial", kwargs={"pk": self.pk})

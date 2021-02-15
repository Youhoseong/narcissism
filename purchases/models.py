from django.db import models
from core import models as core_model
from users import models as user_model

# Create your models here.


class Photo(core_model.TimeStampedModel):
    file = models.FileField(upload_to="room_photos")
    purchases = models.ForeignKey(
        "Purchase", related_name="photos", on_delete=models.CASCADE
    )


class Purchase(core_model.TimeStampedModel):

    closed = models.DateTimeField()
    title = models.CharField(max_length=40, blank=True)
    host = models.ForeignKey(
        user_model.User, related_name="purchase", on_delete=models.CASCADE
    )
    explain = models.TextField(blank=True)

    max_people = models.IntegerField(default=0) # 참여 총 인원
    participants = models.ManyToManyField(user_model.User, related_name="participate", blank=True)
    price = models.IntegerField(default=0) # 총 가격
    address = models.CharField(max_length=80, blank=True) # 게시글 작성자 주소.


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("hello", self.participants)

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
       

class Material(Purchase):
    unit = models.CharField(max_length=5, blank=True) # 단위
    total = models.IntegerField() # 총 수량
    link_address = models.TextField(blank=True)

    category_food = "음식"
    category_daily = "생필품"
    category_other = "기타"

    category_choice = (
        (category_food, "음식"),
        (category_daily, "생필품"),
        (category_other, "기타")
    )
    
    category = models.CharField(choices=category_choice, max_length=20, blank=False, default=category_food)

    def amount_per_person(self):
        return self.total / self.max_people

class Immaterial(Purchase): # 물건 구매가 아닌 활동을 위한 사람을 구하는 게시글.
    category_service = "인터넷 서비스 공유"
    category_education = "교육"
    category_hobby = "여가 활동"
    category_other = "기타"

    category_choice = (
        (category_service, "인터넷 서비스 공유"),
        (category_education,"교육"),
        (category_hobby,"여가 활동"),
        (category_other, "기타"),
    )

    category = models.CharField(choices=category_choice, max_length=20, blank=False, default=category_service)

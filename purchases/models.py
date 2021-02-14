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
    max_people = models.IntegerField(default=0)
    participants = models.ManyToManyField(user_model.User, related_name="participate")
    price = models.IntegerField(default=0)

    # 공유 단위, 가격, 총 개수, 남은 개수, 참여자, (별도 클래스) 카테고리...

    # immaterial
    # material

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
       

class material(Purchase):
    UNIT_KG = "kg"
    UNIT_G = "g"

    UNIT_CHOICE = ((UNIT_KG, "Kg"), (UNIT_G, "g"))

    unit = models.CharField(choices=UNIT_CHOICE, max_length=5, blank=True)
    total = models.IntegerField()
    link_address = models.TextField(blank=True)


class immaterial(Purchase):
    pass

from django.db import models
from core import models as core_model
from users import models as user_model
# Create your models here.


class Purchase(core_model.TimeStampedModel):
    closed = models.DateTimeField()

    title = models.CharField(max_length=40, blank=True)
    host = models.ForeignKey("users.User", related_name="purchase", on_delete=models.CASCADE)
    
    # 사진, 구매 링크, 공유 단위, 가격, 총 개수, 남은 개수, 상품 설명 필드, 지역, 참여자, is_closed,  (별도 클래스) 카테고리...

    # immaterial
    # material

class material(Purchase):
    UNIT_KG = "kg"
    UNIT_G = "g"

    UNIT_CHOICE = (
        (UNIT_KG, "Kg"),
        (UNIT_G, "g"),
    )

    unit = models.CharField(choices=UNIT_CHOICE, max_length=5, blank=True)

    total = models.IntegerField()

class immaterial(Purchase):
    pass
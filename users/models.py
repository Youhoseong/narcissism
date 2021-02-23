from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import uuid


class User(AbstractUser):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.FileField(upload_to="avatars", blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=80, blank=True)

    qr_code = models.FileField(upload_to="qr_codes", blank=True)

    email_verified = models.BooleanField(default=False)
    email_code = models.CharField(max_length=6, default="", blank=True)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    location_verified = models.BooleanField(default=False)
    recent_location_verify_code = models.CharField(max_length=1, blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def dong(self):
        return self.address.split()[-1]

    def verify_email(self):
        if not self.email_verified:
            code = uuid.uuid4().hex[:6]
            self.email_code = code
            self.save()
            # 배포 시 verify_email.html에서 주소를 도메인으로 바꾸어주어야 함
            html_message = render_to_string("users/verify_email.html", {"code": code})
            send_mail(
                "Narcissism 이메일 인증 코드",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
        return

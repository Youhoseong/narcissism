from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao")
    )
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )

    avatar = models.FileField(upload_to="avatars", blank=True)

    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)

    address = models.CharField(max_length=80, blank=True)

    email_verified = models.BooleanField(default=False)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

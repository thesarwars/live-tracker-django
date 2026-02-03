import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .choices import UserTypeChoices, GenderChoices


# Create your models here.
class BaseModelWithUID(models.Model):
    uid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class User(AbstractUser, BaseModelWithUID):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    profile_photo = models.URLField(blank=True, null=True)
    user_type = models.CharField(
        max_length=50, choices=UserTypeChoices.choices, default=UserTypeChoices.CUSTOMER
    )
    gender = models.CharField(
        max_length=50,
        choices=GenderChoices.choices,
        db_index=True,
        default=GenderChoices.MALE,
    )
    # is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

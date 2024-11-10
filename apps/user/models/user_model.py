
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.managers import UserManager
from apps.user.utils.validators import PhoneNumberValidator

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, validators=[PhoneNumberValidator()])

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        db_table = "Users"
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self) -> str:
        return self.phone_number
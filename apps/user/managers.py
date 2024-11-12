from django.contrib.auth.models import BaseUserManager
from rest_framework import status
from apps.user.utils.http_exceptions import CustomValidationException


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise CustomValidationException(
                detail={"message": "Phone number must be entered."},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

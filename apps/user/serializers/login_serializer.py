from rest_framework import serializers

from apps.user.utils.validators import PhoneNumberValidator


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        max_length=15,
        validators=[PhoneNumberValidator()]
    )

    password = serializers.CharField(required=True, max_length=64)

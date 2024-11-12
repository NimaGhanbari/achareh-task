from rest_framework import serializers

from apps.user.utils.validators import PhoneNumberValidator


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        max_length=15,
        validators=[PhoneNumberValidator()]
    )

    verification_code = serializers.CharField(required=True, max_length=6)

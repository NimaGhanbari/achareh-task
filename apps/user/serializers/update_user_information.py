from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UpdateUserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()

        return instance

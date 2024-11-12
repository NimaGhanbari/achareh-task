from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.user.permissions import RateLimitPermission
from apps.user.serializers.login_serializer import LoginSerializer
from apps.user.services.generate_jwt_token import generate_jwt_token
from apps.user.models.user_model import User
from apps.user.utils.http_exceptions import CustomValidationException


class LoginAPIView(APIView):
    permission_classes = [RateLimitPermission]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        user_object = User.objects.filter(phone_number=phone_number).first()
        if not user_object:
            raise CustomValidationException(
                detail={"message": "کاربری با این شماره تلفن یافت نشد"},
                status_code=status.HTTP_404_NOT_FOUND
            )

        if not user_object.check_password(password):
            request.rate_limiter.handle_failed_attempt()
            return Response(
                {"action": "error", "message": "رمز عبور اشتباه است"},
                status=status.HTTP_400_BAD_REQUEST
            )

        jwt_tokens = generate_jwt_token(user_object)
        return Response(
            {"action": "logined",
             "tokens": jwt_tokens},
            status=status.HTTP_200_OK
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.user.permissions import RateLimitPermission
from apps.user.serializers.registeration_serializer import RegisterSerializer
from apps.user.services.generate_jwt_token import generate_jwt_token
from apps.user.services.verify_code import verify_code
from apps.user.models.user_model import User
from apps.user.utils.http_exceptions import CustomValidationException


class RegisterAPIView(APIView):
    permission_classes = [RateLimitPermission]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        verification_code = serializer.validated_data['verification_code']

        if not verify_code(phone_number, verification_code):
            request.rate_limiter.handle_failed_attempt()
            return Response(
                {"action": "error", "message": "کد تایید اشتباه است"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(phone_number=phone_number).exists():
            raise CustomValidationException(
                detail={"message": "کاربری با این شماره تلفن وجود دارد"},
                status_code=status.HTTP_400_BAD_REQUEST)

        user_object = User.objects.create(
            phone_number=phone_number)
        jwt_tokens = generate_jwt_token(user_object)
        return Response(
            {"action": "registered",
             "tokens": jwt_tokens},
            status=status.HTTP_200_OK
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.user.permissions import RateLimitPermission
from apps.user.serializers.registeration_serializer import RegisterSerializer
from apps.user.services.generate_jwt_token import generate_jwt_token
from apps.user.services.verify_code import verify_code
from apps.user.models.user_model import User
from apps.user.utils.http_exceptions import CustomValidationException

from logging import getLogger
logger = getLogger(__name__)


class RegisterAPIView(APIView):
    permission_classes = (RateLimitPermission,)

    def post(self, request, *args, **kwargs):
        logger.info("Received registration request.")

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        verification_code = serializer.validated_data['verification_code']

        logger.info(
            f"Attempting registration for phone number: {phone_number}")
        if not verify_code(phone_number, verification_code):
            logger.warning(
                f"Failed verification for phone number: {phone_number}")
            request.rate_limiter.handle_failed_attempt()
            raise CustomValidationException(
                detail={"message": "Verification code is wrong"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(phone_number=phone_number).exists():
            logger.warning(
                f"User with phone number {phone_number} already exists.")
            raise CustomValidationException(
                detail={"message": "There is a user with this phone number"},
                status_code=status.HTTP_400_BAD_REQUEST)

        user_object = User.objects.create(
            phone_number=phone_number)
        jwt_tokens = generate_jwt_token(user_object)
        logger.info(
            f"User with phone number {phone_number} registered successfully. JWT tokens generated.")

        return Response(
            {"action": "registered",
             "tokens": jwt_tokens},
            status=status.HTTP_200_OK
        )

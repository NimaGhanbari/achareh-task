from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.user.permissions import RateLimitPermission
from apps.user.serializers.login_serializer import LoginSerializer
from apps.user.services.generate_jwt_token import generate_jwt_token
from apps.user.models.user_model import User
from apps.user.utils.http_exceptions import CustomValidationException

from logging import getLogger
logger = getLogger(__name__)


class LoginAPIView(APIView):
    permission_classes = (RateLimitPermission,)

    def post(self, request, *args, **kwargs):
        logger.info("Received login request.")
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        logger.info(f"Login attempt for phone number: {phone_number}")

        user_object = User.objects.filter(phone_number=phone_number).first()
        if not user_object:
            logger.warning(f"No user found for phone number: {phone_number}")
            raise CustomValidationException(
                detail={"message": "User not found with this phone number"},
                status_code=status.HTTP_404_NOT_FOUND
            )

        if not user_object.check_password(password):
            logger.warning(
                f"Invalid password attempt for phone number: {phone_number}")
            request.rate_limiter.handle_failed_attempt()
            raise CustomValidationException(
                detail={"message": "Incorrect password"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        jwt_tokens = generate_jwt_token(user_object)
        logger.info(
            f"User {phone_number} successfully logged in. JWT tokens generated.")

        return Response(
            {"action": "logined",
             "tokens": jwt_tokens},
            status=status.HTTP_200_OK
        )

from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from apps.user.serializers.update_user_information import UpdateUserInfoSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.user.utils.http_exceptions import CustomValidationException
from logging import getLogger

logger = getLogger(__name__)
User = get_user_model()


class UserInfoAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, phone_number):
        logger.info(
            f"Received request to update user information for phone number: {phone_number}")

        user_object = User.objects.filter(phone_number=phone_number).first()
        if not user_object:
            logger.warning(f"User with phone number {phone_number} not found.")
            raise CustomValidationException(
                detail={"message": "User not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateUserInfoSerializer(
            user_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(
            f"User information for phone number {phone_number} updated successfully.")

        return Response(
            {"message": "Data entered successfully"},
            status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from apps.user.serializers.update_user_information import UpdateUserInfoSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.user.utils.http_exceptions import CustomValidationException

User = get_user_model()


class UserInfoAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, phone_number):

        user_object = User.objects.filter(phone_number=phone_number).first()
        if not user_object:
            raise CustomValidationException(
                detail={"message": "کابری یافت نشد"},
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateUserInfoSerializer(
            user_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "اطلاعات با موفقیت ثبت شد"},
            status=status.HTTP_200_OK)

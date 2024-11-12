from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.user.models.user_model import User
from apps.user.serializers.determinate_action_serializer import PhoneNumberSerializer
from apps.user.services.sms_sender_service import send_verification_sms
from apps.user.utils.generate_otp_code import generate_otp

from achareh_project.settings import redis_client, REDIS_TTL_REGISTERATION


class DetermineAuthActionAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        user_exists = User.objects.filter(phone_number=phone_number).exists()

        if user_exists:
            return Response({"action": "login"}, status=status.HTTP_200_OK)
        else:

            phone_number = redis_client.get(phone_number)
            if phone_number:
                return Response(
                    {"action": "error",
                        "message": "لطفا بعداز دو دقیقه مجددا تلاش کنید"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            otp_code = generate_otp()

            # Note: Comments are made to simulate real sending, but SMS sending is actually implemented
            # response = send_verification_sms(
            #     otp_code, f"98{phone_number[1:]}")

            response = {"status": 5}

            if response['status'] == 5:

                redis_client.set(phone_number, otp_code,
                                 int(REDIS_TTL_REGISTERATION))
                return Response(
                    {"action": "register", "send_otp": True},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"action": "register", "send_otp": False},
                    status=status
                    .HTTP_500_INTERNAL_SERVER_ERROR)

from django.urls import path

from apps.user.apis.auth_check_view import DetermineAuthActionAPIView
from apps.user.apis.login_view import LoginAPIView
from apps.user.apis.register_view import RegisterAPIView
from apps.user.apis.update_user_info_view import UserInfoAPIView

urlpatterns = [
    path('determinate-action/', DetermineAuthActionAPIView.as_view(),
         name='determinate-action'),
    path('registeration/', RegisterAPIView.as_view(),
         name='registeration'),
    path('user-info/<str:phone_number>/', UserInfoAPIView.as_view(),
         name='user-info'),
    path('login/', LoginAPIView.as_view(),
         name='login'),
]

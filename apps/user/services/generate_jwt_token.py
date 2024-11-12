from rest_framework_simplejwt.tokens import RefreshToken
from typing import Dict, Union
from apps.user.models.user_model import User


def generate_jwt_token(user: User) -> Dict[str, Union[str, dict]]:

    if user.is_authenticated:
        refresh = RefreshToken.for_user(user)
        token = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return token
    return {}

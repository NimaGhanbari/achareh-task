from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_token(user):

    if user.is_authenticated:
        refresh = RefreshToken.for_user(user)
        token = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return token
    return {}

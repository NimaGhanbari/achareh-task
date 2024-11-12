from rest_framework.permissions import BasePermission
from apps.user.utils.get_ip_address import get_ip_address
from apps.user.utils.rate_limiting import RateLimiter
from apps.user.utils.http_exceptions import CustomValidationException
from rest_framework import status


class RateLimitPermission(BasePermission):
    message = "Too many requests. Please try again after 1 hour."

    def has_permission(self, request, view):
        ip_address = get_ip_address(request)
        action_type = view.__class__.__name__
        rate_limiter = RateLimiter(ip_address, action_type)

        if rate_limiter.block_for_1_hour():
            raise CustomValidationException(
                detail={"message": self.message},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )

        request.rate_limiter = rate_limiter
        return True

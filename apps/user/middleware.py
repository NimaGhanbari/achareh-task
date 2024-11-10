from django.http import JsonResponse
from apps.user.utils.get_ip_address import get_ip_address
from apps.user.utils.rate_limiting import RateLimiter
from apps.user.utils.http_exceptions import CustomValidationException
from rest_framework import status

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = get_ip_address(request)
        
        action_type = request.path.split('/')[1]
        
        # TODO: delete print
        print("action_type: ",action_type)
        
        rate_limiter = RateLimiter(ip_address, action_type)
        
        if rate_limiter.block_for_1_hour():
            raise CustomValidationException(
                detail={"message":"Too many requests. Please try again after 1 hour."},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
                )
        
        response = self.get_response(request)
        
        return response

from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from .models import ApiKey

class AuthMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
            api_key = request.headers.get('Api-Key')
            
            try:
                key = ApiKey.objects.get(key=api_key)
                return None
            except ApiKey.DoesNotExist:
                raise PermissionDenied("Acceso restringido.")
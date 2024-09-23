
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import authentication
from rest_framework import exceptions
from api.models import *

class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        UserModel = get_user_model()
        try:
            email = kwargs.get('email', None)
            if email is None:
                email = kwargs.get('username', None)
            user = UserModel.objects.get(email=email)
            if user.check_password(kwargs.get('password', None)):
                return user
        except UserModel.DoesNotExist:
            return None
    
        
class TelephoneBackend(ModelBackend):
    def authenticate(self, request, telephone=None, **kwargs):
        try:
            user = CustomGuest.objects.get(telephone=telephone)
            return user
        except CustomUser.DoesNotExist:
            return None

class CustomTelephoneAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        telephone = request.headers.get('HTTP_TELEPHONE')
        print(request.headers)
        print(f'telephone: {telephone}')
        if not telephone:
            return None

        try:
            user = CustomGuest.objects.get(telephone=telephone)
            return (user, None)
        except CustomGuest.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid telephone number')

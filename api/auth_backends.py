
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import authentication
from rest_framework import exceptions
from api.models import *

class TelephoneBackend(ModelBackend):
    def authenticate(self, request, telephone=None, password=None,  **kwargs):
        try:
            #print('telephone TelephoneBackend2: ', telephone)
            user = CustomUser.objects.get(telephone=telephone)
            #print('user TelephoneBackend2: ', user)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
        except Exception as e:
            print(e)

    def get_user(self, telephone):
        try:
            return CustomUser.objects.get(telephone=telephone)
        except CustomUser.DoesNotExist:
            return None
    

from typing import Any, Dict
from api.models import *
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth_backends import TelephoneBackend

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['timestamp', 'content', 'conversation']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'#['room_name'] #"__all__" #('room_name',)

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].sender
        return super().create(validated_data)
    

User = get_user_model()


class CustomUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD
    telephone = serializers.CharField(required=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        telephone = attrs.get('telephone')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(telephone=telephone)
            credentials = {
                "telephone": attrs.get("telephone"),
                "password": attrs.get("password"),
            }

            user = TelephoneBackend().authenticate(self.context["request"], **credentials)
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return data


        except User.DoesNotExist as e:
            print(e)
        except Exception as e:
            print(e)

        return super().validate(attrs)
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    
    # password2 = serializers.CharField(write_only=True, required=True)

    telephone = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'telephone', 'age', 'password', 'fullname')

    def validate(self, attrs):
        # if attrs['password'] != attrs['password2']:
        #     raise serializers.ValidationError(
        #         {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['telephone'],
            telephone=validated_data['telephone'],
            fullname=validated_data['fullname'],
            age=validated_data['age'],
        )

        user.set_password(validated_data['telephone'])
        user.save()

        return user
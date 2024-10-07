# from api.models import User, Todo, ChatMessage, Profile
# from django.contrib.auth.password_validation import validate_password
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
        
#         # These are claims, you can add custom claims
#         token['full_name'] = user.profile.full_name
#         token['username'] = user.username
#         token['email'] = user.email
#         token['bio'] = user.profile.bio
#         token['image'] = str(user.profile.image)
#         token['verified'] = user.profile.verified
#         # ...
#         return token


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email']

#         )

#         user.set_password(validated_data['password'])
#         user.save()

#         return user
    

# class TodoSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Todo
#         fields = ['id', 'user', 'title', 'completed']


    
# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Profile
#         fields = [ 'id',  'user',  'full_name', 'image' ]
    
#     def __init__(self, *args, **kwargs):
#         super(ProfileSerializer, self).__init__(*args, **kwargs)
#         request = self.context.get('request')
#         if request and request.method=='POST':
#             self.Meta.depth = 0
#         else:
#             self.Meta.depth = 3


# class MessageSerializer(serializers.ModelSerializer):
#     reciever_profile = ProfileSerializer(read_only=True)
#     sender_profile = ProfileSerializer(read_only=True)

#     class Meta:
#         model = ChatMessage
#         fields = ['id','sender', 'reciever', 'reciever_profile', 'sender_profile' ,'message', 'is_read', 'date']
    
#     def __init__(self, *args, **kwargs):
#         super(MessageSerializer, self).__init__(*args, **kwargs)
#         request = self.context.get('request')
#         if request and request.method=='POST':
#             self.Meta.depth = 0
#         else:
#             self.Meta.depth = 2

from typing import Any, Dict
from api.models import *
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth_backends import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['date', 'message', 'room', 'sender']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'#['room_name'] #"__all__" #('room_name',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    # def create(self, validated_data):
    #     return Room.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.room_name = validated_data.get('room_name', instance.room_name)

    #     instance.save()
    #     return instance
User = get_user_model()

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username_field = User.USERNAME_FIELD
#     email = serializers.EmailField(required=True)

#     def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
#         email = attrs.get('email')
#         password = attrs.get('password')
#         user = User.objects.get(email=email)

#         try:
#             user = User.objects.get(email=email)

#             if user.check_password(password):
#                 refresh = RefreshToken.for_user(user)
#                 data = {
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token)
#                 }
#                 return data
#             else:
#                 raise serializers.ValidationError("Invalid Credentials")
#         except User.DoesNotExist as e:
#             print(e)

#         return super().validate(attrs)
#     # @classmethod
#     # def get_token(cls, user):
#     #     token = super().get_token(user)

#     #     # Add custom claims
        
#     #     # token['username'] = user.username
#     #     token['email'] = user.email
        
#     #     return token
    
#     # def validate(self, attrs):
#     #     data = super().validate(attrs)
#     #     refresh = self.get_token(self.user)
#     #     data['refresh'] = str(refresh)

#     #     data['access'] = str(refresh.access_token)

#     #     return data

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password])
    
#     password2 = serializers.CharField(write_only=True, required=True)

#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=CustomUser.objects.all())]
#     )

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password', 'password2', 'bio', 'full_name')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user = CustomUser.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             bio=validated_data['bio'],
#             full_name=validated_data['full_name'],
#         )

#         user.set_password(validated_data['password'])
#         user.save()

#         return user

class ProfileSerializer(serializers.ModelSerializer):
    # messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model() # CustomUser
        fields = '__all__'
    
    def to_internal_value(self, data):
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, bytes):
                cleaned_data[key] = value.decode('utf-8', errors='replace')
            else:
                cleaned_data[key] = value
        return super().to_internal_value(cleaned_data)
    
class CustomGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGuest
        fields = '__all__'

# class CustomGuest2Serializer(serializers.ModelSerializer):
#     class Meta:
#         models = CustomGuest2
#         fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD
    telephone = serializers.CharField(required=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        telephone = attrs.get('telephone')
        password = attrs.get('password')
        # user = User.objects.get(telephone=telephone)
        
        try:
            user = User.objects.get(telephone=telephone)
            #print('user MyTokenObtainPairSerializer: ', user)   
            credentials = {
                "telephone": attrs.get("telephone"),
                "password": attrs.get("password"),
            }

            user = TelephoneBackend2().authenticate(self.context["request"], **credentials)
            #print('user MyTokenObtain2: ', user)
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return data
            # if user.check_password(password):
            #     refresh = RefreshToken.for_user(user)
            #     data = {
            #         'refresh': str(refresh),
            #         'access': str(refresh.access_token)
            #     }
            #     return data
            # else:
            #     raise serializers.ValidationError("Invalid Credentials")

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
        validators=[UniqueValidator(queryset=CustomGuest2.objects.all())]
    )

    class Meta:
        model = CustomGuest2
        fields = ('username', 'telephone', 'age', 'password', 'fullname')

    def validate(self, attrs):
        # if attrs['password'] != attrs['password2']:
        #     raise serializers.ValidationError(
        #         {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomGuest2.objects.create(
            username=validated_data['telephone'],
            telephone=validated_data['telephone'],
            fullname=validated_data['fullname'],
            age=validated_data['age'],
        )

        user.set_password(validated_data['telephone'])
        user.save()

        return user


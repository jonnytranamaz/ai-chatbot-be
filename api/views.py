from django.shortcuts import render

from api.repositories.impl.conversation_repository import ConversationRepository
from . import views
from django.urls import path
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import OuterRef, Subquery
from django.db.models import Q

from api.models import *
from api.serializer import *

from rest_framework.decorators import api_view, action, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.auth_backends import *
import time
from django.core.paginator import Paginator
from api.repositories import *



#Login User
class CustomUserTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomUserTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
@authentication_classes([JWTAuthentication,])
def get_all_message_in_specific_conversation(request, conversation_id):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 20)
    try:

        conversation = Conversation.objects.get(id=conversation_id)
        messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')

        paginator = Paginator(messages, limit)
        paginated_messages = paginator.get_page(page)

        message_serializer = MessageSerializer(paginated_messages, many=True) # MessageSerializer(messages) #
  
        
        status_code = status.HTTP_200_OK
        response_data = {
            'messsage': 'success',
            'messages': message_serializer.data,
            'page': page,
            'limit': limit,
            'total_pages': paginator.num_pages,
            'total_messages': paginator.count,
        }
   
    except Conversation.DoesNotExist:
        return Response({'message': 'conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        response_data = {'message': 'some errors occur'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(response_data, status=status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_custom_user(request):
    telephone = request.data.get('telephone')
    password = request.data.get('password')
    age = request.data.get('age')
    fullname = request.data.get('fullname')
    try:
        user = CustomUser.objects.get(telephone=telephone)
        response_data = {'message': 'telephone have already existed'}
        status_code = status.HTTP_409_CONFLICT
    except CustomUser.DoesNotExist:
        new_user = CustomUser.objects.create(telephone=telephone, age=age, fullname=fullname, username=telephone)
        new_user.set_password(password)
        new_user.save()
        response_data = {'message': 'success', 'telephone': new_user.telephone}
        status_code = status.HTTP_201_CREATED      
    except Exception as e:
        print(e)
        response_data = {'message': 'some errors occur'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(response_data, status=status_code)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@authentication_classes([JWTAuthentication,])
def create_user_conversation(request):
    user = request.user
    try:
        conversation = Conversation.objects.get(sender=user)
        response_data = {'conversation_id': conversation.id}
        status_code = status.HTTP_200_OK
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Conversation.DoesNotExist:
        new_conversation = ConversationRepository().create_conversation(user)
        response_data = {'conversation_id': new_conversation.id}
        status_code = status.HTTP_201_CREATED
    except Exception as e:
        response_data = {'message': 'Error creating conversation'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(response_data, status=status_code)
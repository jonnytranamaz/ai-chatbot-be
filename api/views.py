from django.shortcuts import render
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
import time
# Create your views here.

urlpatterns = [
    # path('', views.main, name='main'),
    # path('members/', views.members, name='members'),
    # path('members/details/<int:id>', views.details, name='details'),
    # path('testing/', views.testing, name='testing'),  
]

# @api_view(['GET'])
# def getRoutes(request):
#     routes = [
#         '/api/token/',
#         '/api/register/',
#         '/api/token/refresh/'
#     ]
#     return Response(routes)

class GetMesages(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = MessageSerializer

    @action(methods=['post'], detail=True)
    def get_messages(self, request, pk=None):
        message = self.get_object()


class SendMessages(generics.CreateAPIView):
    serializer_class = MessageSerializer

# def CreateRoom(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         room = request.POST['room']

#         try:
#             get_room = Room.objects.get(room_name=room)
#             room_serializers = RoomSerializer(get_room, many=True)
#             json_data = JSONRenderer().render(room_serializers.data)
#             return HttpResponse(json_data, content_type='applicaton/json')
        
#         except Room.DoesNotExist:
#             new_room = Room(room_name=room)
#             new_room.save()
#             room_serializers = RoomSerializer(new_room, many=True)
#             json_data = JSONRenderer().render(room_serializers.data)
#             return HttpResponse(json_data, content_type='applicaton/json')
        
#     data = {'status': 'error', 'message': 'Error Methods'} 
#     return JsonResponse(data) 

def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']
         
        print(message)

        new_message = ChatMessage(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages = ChatMessage.objects.filter(room=get_room)

    messages_data = []
    for message in get_messages:
        message_data = {
            'id': message.id,
            "message": message.message,
            "date": message.date,
            "room": message.room.id,
            "sender": message.sender
        }
        messages_data.append(message_data)

    message_serializer = MessageSerializer(data=messages_data, many=True)
    # json_data = JSONRenderer().render(message_serializer.data)

    if message_serializer.is_valid():
        json_data = message_serializer.data
    else:
        json_data = {"error": message_serializer.errors}
    

    context = {
        "messages": json_data,
        "user": username,
        "room_name": room_name
    }

    return JsonResponse(context)

def TestMessageView(request, room_name):
   
    get_room = Room.objects.get(room_name=room_name)

    get_messages = (ChatMessage.objects.filter(room=get_room))

    # print(get_messages)

    messages_data = []
    for message in get_messages:
        message_data = {
            'id': message.id,
            "message": message.message,
            "date": message.date,
            "room": message.room.id,
            "sender": message.sender
        }
        messages_data.append(message_data)

    print(messages_data)

    # messages_data = [message.serialize() for message in get_messages]

    message_serializer = MessageSerializer(data=messages_data, many=True)
    # json_data = JSONRenderer().render(message_serializer.data)

    if message_serializer.is_valid():
        json_data = message_serializer.data
    else:
        json_data = {"error": message_serializer.errors}
    
    context = {
        "messages": json_data,
        "user": 'guest',
        "room_name": room_name
    }

    return JsonResponse(context)

# def TestRoomView(request):
#     rooms_list = list(Room.objects.all().values())
#     print(rooms_list)

#     room_serializer = RoomSerializer(data=rooms_list, many=True)

#     if room_serializer.is_valid():
#         json_data = room_serializer.data
#     else:
#         json_data = {"error": room_serializer.errors}
    
#     return JsonResponse(json_data, safe=False)

class TestRoomView(APIView):
    def get(self, request, format=None):
        rooms_list = Room.objects.all()
        room_serializer = RoomSerializer(rooms_list, many=True)
        return Response(room_serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def TestRoomView2(request):
    room_list = Room.objects.all()
    room_serializer = RoomSerializer(room_list, many=True)
    return Response(room_serializer.data)

#Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    # def get_tokens(self):
    #     tokens = super().get_tokens()
    #     refresh = tokens['refresh']
    #     access = tokens['access']
    #     return {'refresh': str(refresh), 'access': str(access)}
    
    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     refresh = self.get_token(self.user)
    #     data['refresh'] = str(refresh)
    #     return data

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#api/profile 
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
@authentication_classes([JWTAuthentication,])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

#api/v1//profile/update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication,])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#api/v1/user/<int:pk>/rooms
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication,])
def getUserRooms(request, pk):
    user = CustomUser.objects.get(id=pk)
    rooms = Room.objects.filter(user=user)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

#api/notes
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getNotes(request):
#     public_notes = Note.objects.filter(is_public=True).order_by('-updated')[:10]
#     user_notes = request.user.notes.all().order_by('-updated')[:10]
#     notes = public_notes | user_notes
#     serializer = NoteSerializer(notes, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication,])
def createRoom(request):
    user = request.user
    data = request.data

    room = Room.objects.create(
        user = user,
        body=data['body'],
        room_name=f'{int(time.time() * 1000)}'
    )

    room_serializer = RoomSerializer(room, many=False)
    return Response(room_serializer.data)


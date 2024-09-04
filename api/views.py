from django.shortcuts import render
from . import views
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.db.models import OuterRef, Subquery
from django.db.models import Q

from api.models import *

from api.serializer import *

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer

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

def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
            room_serializers = RoomSerializer(get_room, many=True)
            json_data = JSONRenderer().render(room_serializers.data)
            return HttpResponse(json_data, content_type='applicaton/json')
        
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
            room_serializers = RoomSerializer(new_room, many=True)
            json_data = JSONRenderer().render(room_serializers.data)
            return HttpResponse(json_data, content_type='applicaton/json')
        
    data = {'status': 'error', 'message': 'Error Methods'} 
    return JsonResponse(data) 

def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']
         
        print(message)

        new_message = ChatMessage(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages = ChatMessage.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name
    }

    return JsonResponse(context)

def TestMessageView(request, room_name):
   
    get_room = Room.objects.get(room_name=room_name)

    get_messages = ChatMessage.objects.filter(room=get_room)

    message_serializer = MessageSerializer(get_messages, many=True)
    json_data = JSONRenderer().render(message_serializer.data)

    context = {
        "messages": json_data,
        "user": 'no one',
        "room_name": room_name
    }

    return JsonResponse(context)

def TestRoomView(request):
    get_room = Room.objects.all().values()
    print(get_room)

    context = {
        "rooms": get_room
    }

    return JsonResponse(context)

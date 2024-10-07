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
from api.auth_backends import *
import time
from django.core.paginator import Paginator
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

# CHANGE MODEL HERE
#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomGuest2.objects.all() # CustomUser.objects.all()#
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
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication,])
# def getUserRooms(request, pk):
#     user = CustomUser.objects.get(id=pk)
#     rooms = Room.objects.filter(user=user)
#     serializer = RoomSerializer(rooms, many=True)
#     return Response(serializer.data)

#api/notes
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getNotes(request):
#     public_notes = Note.objects.filter(is_public=True).order_by('-updated')[:10]
#     user_notes = request.user.notes.all().order_by('-updated')[:10]
#     notes = public_notes | user_notes
#     serializer = NoteSerializer(notes, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication,])
# def createRoom(request):
#     user = request.user
#     data = request.data

#     room = Room.objects.create(
#         user = user,
#         body=data['body'],
#         room_name=f'{int(time.time() * 1000)}'
#     )

#     room_serializer = RoomSerializer(room, many=False)
#     return Response(room_serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def guest_login(request):
    telephone = request.data.get('telephone')

    try:
        existed_guest = CustomGuest.objects.get(telephone=telephone)
        return Response({'telephone': existed_guest.telephone}, status=status.HTTP_202_ACCEPTED)
    except:
        serializer = CustomGuestSerializer(data=request.data)
        if serializer.is_valid():
            new_guest = serializer.save()
            return Response({'telephone': new_guest.telephone}, status=status.HTTP_201_CREATED)
        
    return Response({'telephone': -1}, status=status.HTTP_400_BAD_REQUEST)
    # {
    #     'telephone': "013",
    #     'fullname': "micheal ang",
    #     'age': '23'
    # }

# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
# # @authentication_classes([CustomTelephoneAuthentication])
# def create_guest_room(request):
#     telephone = request.data.get('telephone')
#     print(request.data)

#     try:
#         guest = CustomGuest.objects.get(telephone=telephone)
#         room = Room.objects.get(user=guest)
#         response_data = {'room_name': room.room_name}
#         status_code = status.HTTP_200_OK
#     except CustomGuest.DoesNotExist:
#         return Response({'message': 'Guest not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Room.DoesNotExist:
#         new_room = Room.objects.create(user=guest, room_name=f'room_{guest.telephone}')
#         response_data = {'room_name': new_room.room_name}
#         status_code = status.HTTP_201_CREATED
#     except Exception as e:
#         response_data = {'message': 'Error creating room'}
#         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

#     return Response(response_data, status=status_code)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
@authentication_classes([JWTAuthentication,])
def get_all_message_in_specific_room(request, room_name):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 20)
    try:

        room = Room.objects.get(room_name=room_name)
        messages = ChatMessage.objects.filter(room=room).order_by('-date')

        paginator = Paginator(messages, limit)
        paginated_messages = paginator.get_page(page)

        message_serializer = MessageSerializer(paginated_messages, many=True) # MessageSerializer(messages) #
        # response_data = {'message': 'success', 'list_message': message_serializer.data}
        # response_data = message_serializer.data
        
        status_code = status.HTTP_200_OK
        response_data = {
            'messsage': 'success',
            'messages': message_serializer.data,
            'page': page,
            'limit': limit,
            'total_pages': paginator.num_pages,
            'total_messages': paginator.count,
        }
   
    except Room.DoesNotExist:
        return Response({'message': 'room not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        response_data = {'message': 'some errors occur'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(response_data, status=status_code)

    #  telephone = request.data.get('telephone')

    # try:
    #     guest = CustomGuest.objects.get(telephone=telephone)
    #     room = Room.objects.get(user=guest)
    #     messages = ChatMessage.objects.get(room=room)
    #     message_serializer = MessageSerializer(messages, many=True)
    #     response_data = {'message': 'success', 'list_message': message_serializer.data}
    #     status_code = status.HTTP_200_OK
    # except CustomGuest.DoesNotExist:
    #     return Response({'message': 'Guest not found'}, status=status.HTTP_404_NOT_FOUND)
    # except Room.DoesNotExist:
    #     return Response({'message': 'room not found'}, status=status.HTTP_404_NOT_FOUND)
    # except Exception as e:
    #     response_data = {'message': 'Some Error occur'}
    #     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # return Response(response_data, status=status_code)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
# @authentication_classes([CustomTelephoneAuthentication])
def create_custom_guest2(request):
    telephone = request.data.get('telephone')
    password = request.data.get('password')
    age = request.data.get('age')
    fullname = request.data.get('fullname')
    try:
        guest = CustomGuest2.objects.get(telephone=telephone)
        response_data = {'message': 'telephone have already existed'}
        status_code = status.HTTP_409_CONFLICT
    except CustomGuest2.DoesNotExist:
        new_guest = CustomGuest2.objects.create(telephone=telephone, age=age, fullname=fullname, username=telephone)
        new_guest.set_password(password)
        new_guest.save()
        response_data = {'message': 'success', 'telephone': new_guest.telephone}
        status_code = status.HTTP_201_CREATED      
    except Exception as e:
        print(e)
        response_data = {'message': 'some errors occur'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(response_data, status=status_code)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@authentication_classes([JWTAuthentication,])
# @authentication_classes([CustomTelephoneAuthentication])
def create_guest2_room(request):
    user = request.user
    try:
        room = Room.objects.get(user=user)
        response_data = {'room_name': room.room_name}
        status_code = status.HTTP_200_OK
    except CustomGuest2.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Room.DoesNotExist:
        new_room = Room.objects.create(user=user, room_name=f'room_{user.telephone}_{int(time.time() * 1000)}')
        response_data = {'room_name': new_room.room_name}
        status_code = status.HTTP_201_CREATED
    except Exception as e:
        response_data = {'message': 'Error creating room'}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(response_data, status=status_code)

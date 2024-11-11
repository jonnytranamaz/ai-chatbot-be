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
import pandas as pd
import yaml
import os
from .serializer import ChatRequestSerializer
# from .train_intent import get_intent_from_question
from .constants import intent_files


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
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 20))
    last_message_id = request.GET.get('last_message_id')

    try:
        conversation = Conversation.objects.get(id=conversation_id)


        all_messages = Message.objects.filter(conversation=conversation)
        
        if last_message_id:
            messages = all_messages.filter(id__lte=last_message_id).order_by('-id')[:limit]
        else:
            messages = all_messages.order_by('-id')[:limit]

    
        total_messages = all_messages.count()
        paginator = Paginator(messages, limit)
        # total_pages = paginator.num_pages
        total_pages = (total_messages + limit - 1) // limit

        message_serializer = MessageSerializer(messages, many=True)

        status_code = status.HTTP_200_OK
        response_data = {
            'message': 'success',
            'messages': message_serializer.data,
            'page': page,
            'limit': limit,
            'total_pages': total_pages,
            'total_messages': total_messages,
            'last_message_id': message_serializer.data[-1]['id'] if message_serializer.data else None  
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


# class ConvertData(APIView):
#     # Disable authentication and authorization
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         serializer = ChatRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             question = serializer.validated_data['question']
#             answer = serializer.validated_data['answer']

#             intents = self.get_intents_from_api()

#             self.process_data(intents, question, answer)

#             return Response({"message": "Dữ liệu đã được thêm vào file thành công"}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_intents_from_api(self):
#         return []

#     def process_data(self, intents, user_example, bot_response):

        

#         # read example of intent
#         def read_examples_from_file(file_path):
#             examples = set()
#             if os.path.exists(file_path):
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     data = yaml.safe_load(file)
#                     if data and 'nlu' in data:
#                         for item in data['nlu']:
#                             examples.update(item['examples'].splitlines())
#             return examples

#         # save into nlu - intent file
#         question = user_example
#         bot_response = bot_response
#         intent = get_intent_from_question(question).strip()
#         print('intent',intent)
#         if intent in intent_files:
#             file_path = intent_files[intent]
#             existing_examples = read_examples_from_file(file_path)
#             if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
#                 with open(file_path, 'w', encoding='utf-8') as file:
#                     file.write("nlu:\n- intent: {}\n  examples: |\n".format(intent))

#             if question.strip() not in {example.lstrip('- ').strip() for example in existing_examples}:
#                 with open(file_path, 'a', encoding='utf-8') as file:
#                     file.write(f"    - {question.strip()}\n")

#         responses = {f'utter_{intent}': [{'text': bot_response}]}

#         domain_data = {
#             'intents': [],
#             'responses': {}
#         }

#         # save into domain
#         if os.path.exists(intent_files['domain']):
#             with open(intent_files['domain'], 'r', encoding='utf-8') as domain_file:
#                 domain_data = yaml.safe_load(domain_file) or {}

#         existing_intents = set(domain_data.get('intents', []))
#         existing_intents.add(intent)
#         domain_data['intents'] = list(existing_intents)

#         for intent, response_list in responses.items():
#             if intent not in domain_data.get('responses', {}):
#                 domain_data.setdefault('responses', {})[intent] = []
#             for response in response_list:
#                 if response not in domain_data['responses'][intent]:
#                     domain_data['responses'][intent].append(response)

#         with open(intent_files['domain'], 'w', encoding='utf-8') as domain_file:
#             domain_file.write("version: \"3.1\"\n\n")
#             domain_file.write("intents:\n")
#             for intent in domain_data['intents']:
#                 domain_file.write(f"  - {intent}\n")
#             domain_file.write("\nresponses:\n")
#             for intent, response_list in domain_data['responses'].items():
#                 domain_file.write(f"  {intent}:\n")
#                 for response in response_list:
#                     domain_file.write(f"  - text: \"{response['text']}\"\n") 

#         # save into stories
#         stories_data = []
#         existing_intents = set()  
#         added_intents = set() 
#         existing_stories = []
#         if os.path.exists(intent_files['stories']):
#             with open(intent_files['stories'], 'r', encoding='utf-8') as stories_file:
#                 existing_data = yaml.safe_load(stories_file)
#                 if existing_data and 'stories' in existing_data:
#                     existing_stories = existing_data['stories']
#                     for story in existing_stories:
#                         for step in story['steps']:
#                             intent = step.get('intent')
#                             if intent:
#                                 existing_intents.add(intent)
#         intent = get_intent_from_question(question).strip()
#         action = f'utter_{intent}'
#         if intent not in existing_intents and intent not in added_intents:
#             stories_data.append({
#                 'story': f'story_{intent}', 
#                 'steps': [
#                     {'intent': intent},
#                     {'action': action}
#                 ]
#             })
#             added_intents.add(intent)  
#         with open(intent_files['stories'], 'a', encoding='utf-8') as stories_file:
#             for story in stories_data:
#                 stories_file.write(f"- story: {story['story']}\n")
#                 stories_file.write("  steps:\n")
#                 for step in story['steps']:
#                     if 'intent' in step:
#                         stories_file.write(f"  - intent: {step['intent']}\n")
#                     if 'action' in step:
#                         stories_file.write(f"  - action: {step['action']}\n")
                    

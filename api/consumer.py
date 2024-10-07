import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import *
import asyncio
import httpx
from api.constants import *
from groq import Groq
from celery import shared_task
import os
from django.http import JsonResponse
from django.conf import settings

from rasa.core.agent import Agent
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.core.policies.policy import PolicyPrediction
#from rasa.core.interpreter import RasaNLUInterpreter
from rasa.core.channels.channel import UserMessage

# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

# Load RASA Model
model_path = os.path.join(settings.BASE_DIR, "api", "nlu-models", "20241005-204958-joint-array.tar.gz")

# Assuming you have trained the RASA model and have it saved
agent = Agent.load(model_path)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):

        data = event['message']
        await self.create_message(data=data)

        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):

        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        
        if not ChatMessage.objects.filter(message=data['message']).exists():
            new_message = ChatMessage(room=get_room_by_name, sender=data['sender'], message=data['message'])
            new_message.save()  

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        pass 

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        print(f'Data: {text_data}')
        
        event = {
            'type': 'chat_message',
            'message': message #"This is Amaz Chatbot",
        }

        await self.channel_layer.group_send(self.room_name, event)

    async def chat_message(self, event):

        data = event['message']
        # await self.create_message(data=data)

        # print(f"Data2: {data['message']['message']}")

        json_data = {
            'message': data['message']['message']
        }
        json_data_parse = {
            'text': data['message']['message']
        }
        
        parsed_data = await agent.handle_text(json_data_parse)
        print('parsed_data: ', parsed_data)
        # To parse text
        # response_parse_message = await self.call_nlu_api(api_parse_message, json_data_parse)
        #print(f'response_parse_message: {response_parse_message}')
        # TestConsumer.saveSymptomEntity.delay(response_parse_message)
        
        # await self.saveSymptomEntity(parsed_data)
      
        response = await self.call_nlu_api(api_get_message, json_data)
        # print(f'response: {response}')
        if len(response)==0:
            text_response = "you need to send more information! This case ins't define by developer"
        else:
            text_response = response[0]['text']
        # print(f"response: {response}")

        # chat_completion = client.chat.completions.create(
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": 'Explain the importance of fast language models' #data['message']['message'],
        #         }
        #     ],
        #     model="llama3-8b-8192",
        # )
        # print(f'chat_completion: {chat_completion}')

        await self.saveChatTurn(data['message']['message'], text_response)
        
        response_data = {
            #'sender': data['sender'],
            'message': text_response # data['message'] # chat_completion.choices[0].message.content # 
        }

        await self.send(text_data=json.dumps({'message': response_data}))

    async def call_nlu_api(self, url, data):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            return response.json()
    # @database_sync_to_async
    # def create_message(self, data):

    #     get_room_by_name = Room.objects.get(room_name=data['room_name'])
        
    #     if not ChatMessage.objects.filter(message=data['message']).exists():
    #         new_message = ChatMessage(room=get_room_by_name, sender=data['sender'], message=data['message'])
    #         new_message.save()  
         


    # 
    # @shared_task
    # @staticmethod
    @database_sync_to_async
    def saveChatTurn(self, request, response):
        chatTurn = ChatTurn(user_request=request, bot_response=response)
        chatTurn.save()

    @database_sync_to_async
    def saveSymptomEntity(self, json):
        entities = json.get('entities')
        # print(entities)
        for entity in entities:
            if (entity.get('entity') == 'symptom'):
                # print(entity.get('value'))
                symptom = Symptom(name= entity.get('value'))
                symptom.save()

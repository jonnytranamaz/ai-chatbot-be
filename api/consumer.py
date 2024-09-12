import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import *
import asyncio
import httpx
from api.constants import *
from groq import Groq
import os
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


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
        self.room_name = f"room_test"
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

        print(f"Data2: {data['message']}")

        json_data = {
            'message': data['message']['message']
        }
        api_url = api_nlu_address

        # response = await self.call_nlu_api(api_url, json_data)
        # print(f"response: {response}")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": 'Explain the importance of fast language models' #data['message']['message'],
                }
            ],
            model="llama3-8b-8192",
        )
        print(f'chat_completion: {chat_completion}')
        
        response_data = {
            #'sender': data['sender'],
            'message': chat_completion.choices[0].message.content # response[0]['text'] #data['message']
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
         
       
       
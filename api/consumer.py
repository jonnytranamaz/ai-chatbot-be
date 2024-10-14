import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import *
import asyncio
import httpx
from api.constants import *
from groq import Groq
import os
from django.http import JsonResponse
from django.utils.timezone import now

# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )


# Load RASA Model
#model_path = os.path.join("/Users/tranminhtriet/Documents/GitHub/ai-chatbot-be/api/ai-models/20240923-152654-jolly-chablis.tar.gz")

# Assuming you have trained the RASA model and have it saved
#agent = Agent.load(model_path)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = f"{self.scope['url_route']['kwargs']['conversation_id']}"
        await self.channel_layer.group_add(self.conversation_id, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.conversation_id, self.channel_name)
        pass 

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        print(f'Data: {text_data}')
        
        event = {
            'type': 'message',
            'message': message #"This is Amaz Chatbot",
        }

        await self.channel_layer.group_send(self.conversation_id, event)

    async def message(self, event):

        data = event['message']
        # await self.create_message(data=data)

        # print(f"Data2: {data['message']['message']}")

        json_data = {
            'message': data['message']['message']
        }
        json_data2 = {
            'text': data['message']['message']  # 'Explain the importance of fast language models'
        }
        api_url = api_get_message



        response = await self.call_nlu_api(api_url, json_data)
        print(f'response: {response}')
        if len(response)==0:
            text_response = "you need to send more information! This case isn't define by developer"
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
            'message':  text_response #parsed_data #text_response # data['message'] # chat_completion.choices[0].message.content # 
        }

        await self.send(text_data=json.dumps({'message': response_data}))

    async def call_nlu_api(self, url, data):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            return response.json()
    
    @database_sync_to_async
    def saveChatTurn(self, request, response):
        user_message = Message(timestamp =now,content=request, owner_type='enduser', message_type='text')
        user_message.save()
        bot_message = Message(content=response, owner_type='bot')
        bot_message.save()

    @database_sync_to_async
    def saveSymptomEntity(self, json):
        entities = json.get('entities')
        # print(entities)
        for entity in entities:
            if (entity.get('entity') == 'symptom'):
                # print(entity.get('value'))
                symptom = Symptom(name= entity.get('value'))
                symptom.save()

       
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
from rasa.core.agent import Agent
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.core.policies.policy import PolicyPrediction
#from rasa.core.interpreter import RasaNLUInterpreter
from rasa.core.channels.channel import UserMessage

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


# Load RASA Model
model_path = os.path.join("/Users/tranminhtriet/Documents/GitHub/ai-chatbot-be/api/ai-models/20240923-152654-jolly-chablis.tar.gz")

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
        json_data2 = {
            'text': data['message']['message']  # 'Explain the importance of fast language models'
        }
        api_url = api_nlu_address

        #parsed_data = await agent.parse_message( data['message']['message'] )#
        parsed_data = await agent.handle_text(json_data2)

        print('parsed_data: ',parsed_data)
        # response = await self.call_nlu_api(api_url, json_data)
        # print(f'response: {response}')
        # if len(response)==0:
        #     text_response = "you need to send more information! This case ins't define by developer"
        # else:
        #     text_response = response[0]['text']
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
        
        response_data = {
            #'sender': data['sender'],
            'message': parsed_data #text_response # data['message'] # chat_completion.choices[0].message.content # 
        }

        await self.send(text_data=json.dumps({'message': response_data}))

    async def call_nlu_api(self, url, data):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            return response.json()
    



# def rasa_parse_message(request):
#     if request.method == 'POST':
#         user_message = request.POST.get('message', '')

#         if user_message:
#             # Parse the message using the loaded RASA model
#             # This will parse the message and predict the intent and action
#             parsed_data = agent.handle_text(user_message)

#             # Return the parsed RASA response as JSON
#             return JsonResponse(parsed_data, safe=False)
#         else:
#             return JsonResponse({"error": "No message provided"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=405)

        

    # @database_sync_to_async
    # def create_message(self, data):

    #     get_room_by_name = Room.objects.get(room_name=data['room_name'])
        
    #     if not ChatMessage.objects.filter(message=data['message']).exists():
    #         new_message = ChatMessage(room=get_room_by_name, sender=data['sender'], message=data['message'])
    #         new_message.save()  
         
       
       
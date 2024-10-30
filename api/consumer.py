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
from api.externalservices.genai import GenerativeAIService
#from django_rabbitmq import publishers
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
        print(f'response text: {response[0]["text"]}')
        # if len(response)==0 or response[0]["text"] == "Sorry, I can't handle that request.":
        #     text_response = GenerativeAIService().get_response(json_data['message'])
        #     print(f'genai response: {text_response}')
        #     #print("I'm here")
        # # if len(response)==0:
        # #     text_response = "you need to send more information! This case isn't define by developer"
        # else:
        text_response = response[0]['text']
        print(f'NLU response: {text_response}')
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
        
        # # Connect to RabbitMQ and declare a queue
        # publisher = publishers.Publisher(queue_name='training')

        # # Send a message
        # publisher.send_message('Need to train the model!')

        response_data = {
            #'sender': data['sender'],
            'message':  text_response #parsed_data #text_response # data['message'] # chat_completion.choices[0].message.content # 
        }

        await self.send(text_data=json.dumps({'message': response_data}))

    async def call_nlu_api(self, url, data):
     async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return []
            except Exception as e:
                print(f"An error occurred: {e}")
                return []
    
    @database_sync_to_async
    def saveChatTurn(self, request, response):
        conversation = Conversation.objects.get(id=self.conversation_id)
        user_message = Message(timestamp =now,content=request, owner_type='enduser', message_type='text', conversation=conversation )
        user_message.save()
        bot_message = Message(content=response, owner_type='bot', conversation=conversation, message_type='text')
        bot_message.save()
        chat_turn = ChatTurn(user_request=request, bot_response=response)
        chat_turn.save()

    @database_sync_to_async
    def saveSymptomEntity(self, json):
        entities = json.get('entities')
        # print(entities)
        for entity in entities:
            if (entity.get('entity') == 'symptom'):
                # print(entity.get('value'))
                symptom = Symptom(name= entity.get('value'))
                symptom.save()
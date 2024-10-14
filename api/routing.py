from django.urls import path
from api.consumer import *


websocket_urlpatterns = [
    path('ws/conversation/<str:conversation_id>', ChatConsumer.as_asgi()),
]

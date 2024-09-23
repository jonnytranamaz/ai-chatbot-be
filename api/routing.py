from django.urls import path
from api.consumer import *


websocket_urlpatterns = [
    path('ws/notification-test/<str:room_name>', TestConsumer.as_asgi()),
    path('ws/notification/<str:room_name>', ChatConsumer.as_asgi()),
]

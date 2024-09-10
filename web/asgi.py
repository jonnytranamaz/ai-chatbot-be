"""
ASGI config for ai_chatbot_be project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api import routing
# from socketio import ASGIApp
from channels.auth import AuthMiddlewareStack

from django.urls import path
from api.consumer import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_chatbot_be.settings')

django_asgi_app  = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # "websocket": ASGIApp(
    #     application = django_asgi_app,
    #     namespace='socket.io',
    # )
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
            # [
            #     path(r'ws/notification-test', TestConsumer.as_asgi()),
            #     #path(r'ws/', TestConsumer.as_asgi()),
            #     path(r'ws', TestConsumer.as_asgi()),
            #     #path(r'/ws/', TestConsumer.as_asgi()),
            #     #path(r'/ws', TestConsumer.as_asgi()),
            # ]
        )
    )
})

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(application, host='0.0.0.0', port=8001)
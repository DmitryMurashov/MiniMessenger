from django.urls import path
from . import consumers

app_name = 'mainapp'

websocket_urlpatterns = [
    path('chats/events/', consumers.GlobalUserEventsConsumer.as_asgi(), name='global_user_events'),
    path('chats/chat/<int:chat_id>/events/', consumers.ChatEventsConsumer.as_asgi(), name='chat_events'),
]

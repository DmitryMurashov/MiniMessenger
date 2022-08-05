from djangochannelsrestframework.generics import AsyncAPIConsumer
from djangochannelsrestframework.observer.generics import action as consumer_action
from mainapp.permissions import WSConnectIfMember, WSConnectIfAuthenticated
from mainapp.serializers import *
from utils.sync_to_async import *
from django.db import models
from rest_framework.serializers import Serializer
from typing import Type
from utils.events import event_handler
import json


class EventConsumer(AsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        super(EventConsumer, self).__init__(*args, **kwargs)
        self.user = None
        self.events = {}

    async def connect(self):
        await self.get_requirements()
        await super(EventConsumer, self).accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        try:
            await super(EventConsumer, self).receive(text_data, bytes_data, **kwargs)
        except json.JSONDecodeError as error:
            await self.send_json(content={"error": f"JSONDecodeError: {error}"})

    async def disconnect(self, close_code):
        await super(EventConsumer, self).disconnect(close_code)

    async def get_requirements(self) -> None:
        ...

    async def send_event(self, instance: models.Model, serializer: Type[Serializer], message_type: str, model_action: str, **kwargs) -> None:
        message_data = await sync_to_async_serialize(instance, serializer)
        await self.send_json(content={
            'message_type': message_type,
            'model_action': model_action,
            'data': message_data,
            **kwargs
        })

    @consumer_action()
    async def subscribe_for_event(self, event_name, request_id, **_) -> None:
        handler = self.events.get(event_name)
        if handler:
            await handler.subscribe(request_id=request_id)
        else:
            await self.send_json(content={"error": f"Event handler '{event_name}' not found"})


class ChatEventsConsumer(EventConsumer):
    permission_classes = (WSConnectIfAuthenticated, WSConnectIfMember,)

    def __init__(self, *args, **kwargs):
        super(ChatEventsConsumer, self).__init__(*args, **kwargs)
        self.chat = None
        self.events = {
            'on.message': self.on_message,
            'on.member.joined': self.on_member_joined
        }

    async def get_requirements(self):
        self.user = self.scope['user']
        assert self.user
        chat_id = self.scope['url_route']['kwargs'].get("chat_id")
        assert chat_id
        self.chat = await sync_to_async_get(Chat, id=chat_id)

    @event_handler(Message, selected_action='create')
    async def on_message(self, instance: Message, message_type: str, model_action: str, **_):
        instance_chat = await sync_to_async_get_related(instance, "chat")
        if instance_chat == self.chat:
            await self.send_event(instance, MessageSerializer, message_type, model_action)

    @event_handler(ChatMember, selected_action='create')
    async def on_member_joined(self, instance: ChatMember, message_type: str, model_action: str, **_):
        instance_chat = await sync_to_async_get_related(instance, "chat")
        if instance_chat == self.chat:
            await self.send_event(instance, ChatMemberSerializer, message_type, model_action)


class GlobalUserEventsConsumer(AsyncAPIConsumer):
    pass

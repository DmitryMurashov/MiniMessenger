from djangochannelsrestframework.generics import AsyncAPIConsumer
from djangochannelsrestframework.observer.generics import action as consumer_action
from mainapp.permissions import WSConnectIfMember, WSConnectIfAuthenticated
from mainapp.serializers import *
from utils.sync_to_async import *
from utils.events import event_handler
import json


class EventConsumer(AsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        super(EventConsumer, self).__init__(*args, **kwargs)
        self.user = None
        self.events = {}

    async def connect(self) -> None:
        await self.get_requirements()
        await super(EventConsumer, self).accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs) -> None:
        try:
            await super(EventConsumer, self).receive(text_data, bytes_data, **kwargs)
        except json.JSONDecodeError as error:
            await self.send_json(content={"error": f"JSONDecodeError: {error}"})

    async def disconnect(self, close_code) -> None:
        await super(EventConsumer, self).disconnect(close_code)

    async def get_requirements(self) -> None:
        ...

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
            'on.member.joined': self.on_member_joined,
            'on.member.left': self.on_member_left
        }

    async def get_requirements(self):
        self.user = self.scope['user']
        assert self.user

        chat_id = self.scope['url_route']['kwargs'].get("chat_id")
        assert chat_id

        self.chat = await sync_to_async_get(Chat, id=chat_id)

    @event_handler(Message, MessageSerializer, selected_action='create')
    async def on_message(self, message: dict, **_) -> None:
        if message['object']["chat"]["id"] == self.chat.id:
            await self.send_json(message)

    @event_handler(ChatMember, ChatMemberSerializer, selected_action='create')
    async def on_member_joined(self, message: dict, **_) -> None:
        if message['object']["chat"]["id"] == self.chat.id:
            await self.send_json(message)

    @event_handler(ChatMember, ChatMemberSerializer, selected_action='delete')
    async def on_member_left(self, message: dict, **_) -> None:
        if message['object']["chat"]["id"] == self.chat.id:
            await self.send_json(message)

    @event_handler(Chat, ChatSerializer, selected_action='delete')
    async def on_chat_deleted(self, message: dict) -> None:
        if message['object']['id'] == self.chat.id:
            await self.send_json(message)


class GlobalUserEventsConsumer(EventConsumer):
    permission_classes = (WSConnectIfAuthenticated,)

    def __init__(self, *args, **kwargs):
        super(GlobalUserEventsConsumer, self).__init__(*args, **kwargs)
        self.chat = None
        events = [
            self.on_user_message,
            self.on_user_invited,
            self.on_user_joined_chat,
            self.on_user_left_chat,
            self.on_user_created_chat
        ]
        self.events = {events.__name__.replace('_', '.'): event for event in events}

    async def get_requirements(self):
        self.user = self.scope['user']
        assert self.user

        chat_id = self.scope['url_route']['kwargs'].get("chat_id")
        assert chat_id

        self.chat = await sync_to_async_get(Chat, id=chat_id)

    @event_handler(Message, MessageSerializer, selected_action='create')
    async def on_user_message(self, message: dict) -> None:
        if message['object']['author']['user']['id'] == self.user.id:
            await self.send_json(message)

    @event_handler(ChatInvite, ChatInviteSerializer, selected_action='create')
    async def on_user_invited(self, message: dict) -> None:
        if message['object']['target']['id'] == self.user.id:
            await self.send_json(message)

    @event_handler(ChatMember, ChatMemberSerializer, selected_action='create')
    async def on_user_joined_chat(self, message: dict) -> None:
        if message['object']['user']['id'] == self.user.id:
            await self.send_json(message)

    @event_handler(ChatMember, ChatMemberSerializer, selected_action='delete')
    async def on_user_left_chat(self, message: dict) -> None:
        if message['object']['user']['id'] == self.user.id:
            await self.send_json(message)

    @event_handler(Chat, ChatSerializer, selected_action='create')
    async def on_user_created_chat(self, message: dict) -> None:
        if message['object']['owner']['id'] == self.user.id:
            await self.send_json(message)

    @event_handler(Chat, ChatSerializer, selected_action='delete')
    async def on_user_deleted_chat(self, message: dict) -> None:
        if message['object']['user']['id'] == self.user.id:
            await self.send_json(message)

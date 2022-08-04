import json
from djangochannelsrestframework.generics import AsyncAPIConsumer
from djangochannelsrestframework.observer import ModelObserver, model_observer
from djangochannelsrestframework import permissions
from mainapp.permissions import WSIsMember
from mainapp.models import *
from mainapp.serializers import *
from utils.sync_to_async import sync_to_async_get, sync_to_async_serialize


class GlobalUserEventsConsumer(AsyncAPIConsumer):
    pass


class ChatEventsConsumer(AsyncAPIConsumer):
    permission_classes = (permissions.IsAuthenticated, WSIsMember,)

    async def connect(self):
        await self.on_message.subscribe()
        await super().accept()

    @model_observer(Message)
    async def on_message(self, message: dict, message_type: str, action: str, **kwargs):
        if action == 'create':
            instance = await sync_to_async_get(Message, id=message['pk'])
            await self.send_json(content=await sync_to_async_serialize(instance, MessageSerializer))

    async def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        text_data_json = json.loads(text_data)
        print(json.dumps(text_data_json, indent=4))

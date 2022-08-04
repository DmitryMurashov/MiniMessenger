from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from django.views import View
from mainapp.models import Chat, Message, ChatMember
from authapp.models import User
from typing import Dict, Any
from djangochannelsrestframework.permissions import BasePermission as WSBasePermission
from channels.consumer import AsyncConsumer

from utils.sync_to_async import sync_to_async_get, sync_to_async_filter


class ReadOnly(BasePermission):
    @staticmethod
    def check_permission(request) -> bool:
        return request.method in SAFE_METHODS

    def has_permission(self, request: Request, view: View) -> bool:
        return self.check_permission(request)


class IsMember(BasePermission):
    message = "Для осуществления запроса пользователь должен быть участником чата"

    @staticmethod
    def check_permission(chat: Chat, user: User) -> bool:
        return chat.is_member(user)

    def has_permission(self, request: Request, view: View) -> bool:
        chat_id = request.resolver_match.kwargs.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        return self.check_permission(chat, request.user)


class CanManageMessage(BasePermission):
    message = "Для осуществления запроса пользователь должен быть владельцем сообщения или администратором чата"

    @staticmethod
    def check_permission(message: Message, member: ChatMember) -> bool:
        return message.author == member or member.is_admin

    def has_permission(self, request: Request, view: View) -> bool:
        chat_id = request.resolver_match.kwargs.get('chat_id')
        message_id = request.resolver_match.kwargs.get('message_id')

        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.get(id=message_id)
        member = chat.fetch_member(request.user)

        return self.check_permission(message, member)


class IsAdmin(BasePermission):
    message = "Для осуществления запроса пользователь должен быть администратором чата"

    @staticmethod
    def check_permission(chat: Chat, member: ChatMember) -> bool:
        return chat.owner == member.user or member.is_admin

    def has_permission(self, request: Request, view: View) -> bool:
        chat_id = request.resolver_match.kwargs.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        member = chat.fetch_member(request.user)
        return self.check_permission(chat, member)


class IsPublicChat(BasePermission):
    message = "Для осуществления запроса пользователь должен быть участником чата"

    @staticmethod
    def check_permission(chat: Chat, user: User) -> bool:
        return not chat.is_private or chat.is_member(user)

    def has_permission(self, request: Request, view: View):
        chat_id = request.resolver_match.kwargs.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        return self.check_permission(chat, request.user)


class WSIsMember(WSBasePermission):
    async def can_connect(self, scope: Dict[str, Any], consumer: AsyncConsumer, message=None) -> bool:
        chat_id = scope['url_route']['kwargs']['chat_id']
        chat = await sync_to_async_get(Chat, id=chat_id)
        try:
            await sync_to_async_get(ChatMember, user=scope['user'], chat=chat)
            return True
        except ChatMember.DoesNotExist:
            return False

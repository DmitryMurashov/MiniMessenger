from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from django.views import View
from mainapp.models import Chat, Message
from django.core.exceptions import ObjectDoesNotExist


class ReadOnly(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.method in SAFE_METHODS


class IsMember(BasePermission):
    message = "Для осуществления запроса пользователь должен быть участником чата"

    def has_permission(self, request: Request, view: View) -> bool:
        if chat_id := request.resolver_match.kwargs.get('chat_id'):
            try:
                chat = Chat.objects.get(id=chat_id)
                chat.fetch_member(request.user)
                return True
            except ObjectDoesNotExist:
                return False
        return False


class CanManageMessage(BasePermission):
    message = "Для осуществления запроса пользователь должен быть владельцем сообщения или администратором чата"

    def has_permission(self, request: Request, view: View) -> bool:
        if (chat_id := request.resolver_match.kwargs.get('chat_id')) and (message_id := request.resolver_match.kwargs.get('message_id')):
            try:
                chat = Chat.objects.get(id=chat_id)
                message = Message.objects.get(id=message_id)
                member = chat.fetch_member(request.user)
            except ObjectDoesNotExist:
                return False
            return message.author == member or member.is_admin
        return False


class DeleteIfChatOwner(BasePermission):
    message = "Для осуществления запроса пользователь должен быть владельцем сообщения или администратором чата"

    def has_permission(self, request: Request, view: View) -> bool:
        if request.method != "DELETE":
            return True
        if chat_id := request.resolver_match.kwargs.get('chat_id'):
            try:
                chat = Chat.objects.get(id=chat_id)
            except ObjectDoesNotExist:
                return False
            return chat.owner == request.user
        return False


class IsAdmin(BasePermission):
    message = "Для осуществления запроса пользователь должен быть администратором чата"

    def has_permission(self, request: Request, view: View) -> bool:
        if chat_id := request.resolver_match.kwargs.get('chat_id'):
            try:
                chat = Chat.objects.get(id=chat_id)
                member = chat.fetch_member(request.user)
            except ObjectDoesNotExist:
                return False
            return member.is_admin
        return False


class IsPrivateChat(BasePermission):
    message = "Для осуществления запроса пользователь должен быть участником чата"

    def has_permission(self, request: Request, view: View):
        if chat_id := request.resolver_match.kwargs.get('chat_id'):
            try:
                chat = Chat.objects.get(id=chat_id)
            except ObjectDoesNotExist:
                return False
            if not chat.is_private or chat.is_member(request.user):
                return True
        return False

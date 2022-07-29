from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from django.views import View
from mainapp.models import Chat, Message
from django.core.exceptions import ObjectDoesNotExist


class IsMember(BasePermission):
    message = "Для осуществления запроса пользователь должен быть участником чата"

    def has_permission(self, request: Request, view: View) -> bool:
        if chat_id := request.resolver_match.kwargs.get('chat_id'):
            chat = Chat.objects.get(id=chat_id)
            try:
                chat.fetch_member(request.user)
                return True
            except ObjectDoesNotExist:
                return False
        return False


class CanManageMessageOrReadOnly(BasePermission):
    message = "Для осуществления запроса пользователь должен быть участником чата"

    def has_permission(self, request: Request, view: View) -> bool:
        if (chat_id := request.resolver_match.kwargs.get('chat_id')) and (message_id := request.resolver_match.kwargs.get('message_id')):
            chat = Chat.objects.get(id=chat_id)
            message = Message.objects.get(id=message_id)
            member = chat.fetch_member(request.user)
            if (message.author == member or member.is_admin) or request.method in SAFE_METHODS:
                return True
        return False


class DeleteIfChatOwner(BasePermission):
    message = "Только владелец чата может его удалить"

    def has_permission(self, request: Request, view: View) -> bool:
        if request.method != "DELETE":
            return True
        if chat_id := request.resolver_match.kwargs.get('chat_id'):
            chat = Chat.objects.get(id=chat_id)
            if chat.owner == request.user:
                return True
        return False

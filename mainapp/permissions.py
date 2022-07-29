from rest_framework.permissions import BasePermission
from django.http import HttpRequest
from django.views import View
from mainapp.models import Chat


class IsMember(BasePermission):
    message = "Для осуществления запроса пользователь должен быть участником чата"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if chat_id := request.resolver_match.kwargs.get('chat_id'):
            chat = Chat.objects.get(id=chat_id)
            if chat.get_member(request.user) is not None:
                return True
        return False

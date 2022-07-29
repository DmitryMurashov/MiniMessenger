from rest_framework.views import APIView, status
from mainapp.models import Chat
from rest_framework.views import Response
from django.core.exceptions import ObjectDoesNotExist


class ObjectMixin(APIView):
    def __return_response(self, request, response,*args, **kwargs):
        self.headers = self.default_response_headers
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def get_object(self, request, *args, **kwargs) -> None:
        ...

    def dispatch(self, request, *args, **kwargs):
        for subclass in self.__class__.mro():
            if issubclass(subclass, ObjectMixin):
                try:
                    subclass.get_object(self, request, *args, **kwargs)
                except ObjectDoesNotExist:
                    response = Response({"error": "Объект не найден"}, status.HTTP_404_NOT_FOUND)
                    return self.__return_response(request, response, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)


class ChatMixin(ObjectMixin):
    def __init__(self):
        super(ChatMixin, self).__init__()
        self.chat = None

    def get_object(self, request, *args, **kwargs) -> None:
        self.chat = Chat.objects.get(id=kwargs.get("chat_id"))


class MemberMixin(ChatMixin):
    def __init__(self):
        super(MemberMixin, self).__init__()
        self.member = None

    def get_object(self, request, *args, **kwargs) -> None:
        if self.chat is not None:
            self.member = self.chat.get_member(request.user)

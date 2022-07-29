from rest_framework.views import APIView, status
from mainapp.models import Chat, Message
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
        initialized_request = super(ObjectMixin, self).initialize_request(request)

        subclasses = list(reversed(list(filter(lambda x: issubclass(x, ObjectMixin), self.__class__.mro()))))[1:-1]
        for subclass in subclasses:
            subclass: ObjectMixin
            try:
                subclass.get_object(self, initialized_request, *args, **kwargs)
            except ObjectDoesNotExist:
                response = Response({"error": "Объект не найден"}, status.HTTP_404_NOT_FOUND)
                return self.__return_response(initialized_request, response, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)


class ChatMixin(ObjectMixin):
    def __init__(self):
        super(ChatMixin, self).__init__()
        self.chat = None

    def get_object(self, request, *args, **kwargs) -> None:
        self.chat = Chat.objects.get(id=kwargs.get("chat_id"))


class ChatMemberMixin(ChatMixin):
    def __init__(self):
        super(ChatMemberMixin, self).__init__()
        self.member = None

    def get_object(self, request, *args, **kwargs) -> None:
        self.member = self.chat.fetch_member(request.user)


class MessageMixin(ObjectMixin):
    def __init__(self):
        super(MessageMixin, self).__init__()
        self.message = None

    def get_object(self, request, *args, **kwargs) -> None:
        self.message = Message.objects.get(id=kwargs.get("message_id"))

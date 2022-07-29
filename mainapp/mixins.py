from rest_framework.views import APIView
from mainapp.models import Chat


class ChatMixin(APIView):
    def __init__(self):
        super(ChatMixin, self).__init__()
        self.chat = None

    def dispatch(self, request, *args, **kwargs):
        self.chat = Chat.objects.get(id=kwargs.get("chat_id"))
        return super().dispatch(request, *args, **kwargs)


class MemberMixin(ChatMixin, APIView):
    def __init__(self):
        super(MemberMixin, self).__init__()
        self.member = None

    def dispatch(self, request, *args, **kwargs):
        self.member = self.chat.get_member(request.user)
        return super().dispatch(request, *args, **kwargs)

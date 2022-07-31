from mainapp.models import Chat, Message, ChatInvite, ChatMember
from utils.mixins import ObjectMixin
from rest_framework.views import Request


class ChatMixin(ObjectMixin):
    def __init__(self):
        super(ChatMixin, self).__init__()
        self.chat = None

    def get_mixin_object(self, request: Request, *args, **kwargs) -> None:
        self.chat = Chat.objects.get(id=kwargs.get("chat_id"))


class MessageMixin(ObjectMixin):
    def __init__(self):
        super(MessageMixin, self).__init__()
        self.message = None

    def get_mixin_object(self, request: Request, *args, **kwargs) -> None:
        self.message = Message.objects.get(id=kwargs.get("message_id"))


class ChatMemberMixin(ChatMixin):
    def __init__(self):
        super(ChatMemberMixin, self).__init__()
        self.member = None

    def get_mixin_object(self, request: Request, *args, **kwargs) -> None:
        super(ChatMemberMixin, self).get_mixin_object(request, *args, **kwargs)
        self.member = ChatMember.objects.get(id=kwargs.get("member_id"))


class InviteMixin(ObjectMixin):
    def __init__(self):
        super(InviteMixin, self).__init__()
        self.invite = None

    def get_mixin_object(self, request: Request, *args, **kwargs) -> None:
        self.invite = ChatInvite.objects.get(id=kwargs.get("invite_id"))


class ChatRequestMemberMixin(ChatMixin):
    def __init__(self):
        super(ChatRequestMemberMixin, self).__init__()
        self.request_member = None

    def get_mixin_object(self, request, *args, **kwargs) -> None:
        super(ChatRequestMemberMixin, self).get_mixin_object(request, *args, **kwargs)
        self.request_member = self.chat.fetch_member(request.user)

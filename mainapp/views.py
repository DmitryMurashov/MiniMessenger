from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from mainapp.mixins import *
from mainapp.permissions import *
from mainapp.serializers import *
from authapp.models import User
from rest_framework.exceptions import APIException
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView
)


class ChatListApiView(CreateAPIView, ListAPIView, APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return [obj.chat for obj in self.request.user.chats.all()]

    @property
    def get_serializer(self):
        if self.request.method == "POST":
            self.request.data["owner_id"] = self.request.user.id
            return CreateChatSerializer
        return ChatSerializer


class ChatApiView(ChatMixin, UpdateAPIView, RetrieveAPIView, DestroyAPIView, APIView):
    permission_classes = (IsAuthenticated, DeleteIfChatOwner, IsPrivateChat)
    get_serializer = ChatSerializer

    def get_object(self):
        return self.chat


class ChatMessageListApiView(ChatRequestMemberMixin, CreateAPIView, ListAPIView, APIView):
    permission_classes = (IsAuthenticated, IsMember)

    def get_queryset(self):
        return self.chat.messages.all()

    @property
    def get_serializer(self):
        if self.request.method == "POST":
            self.request.data["author_id"] = self.request_member.id
            self.request.data["chat_id"] = self.chat.id
            return CreateMessageSerializer
        return MessageSerializer


class ChatMessageApiView(MessageMixin, UpdateAPIView, RetrieveAPIView, DestroyAPIView, APIView):
    permission_classes = (IsAuthenticated, IsMember, CanManageMessage | ReadOnly)
    get_serializer = MessageSerializer

    def get_object(self):
        return self.message


class ChatMemberListApiView(ChatMixin, ListAPIView, APIView):
    permission_classes = (IsAuthenticated, IsMember)
    get_serializer = ChatMemberSerializer

    def get_queryset(self):
        return self.chat.members


class ChatMemberApiView(ChatMemberMixin, UpdateAPIView, RetrieveAPIView, DestroyAPIView, APIView):
    permission_classes = (IsAuthenticated, IsMember, IsAdmin | ReadOnly)
    serializer_class = ChatMemberSerializer

    def get_object(self):
        return self.member


class ChatInviteListApiView(ChatRequestMemberMixin, CreateAPIView, ListAPIView, APIView):
    permission_classes = (IsAuthenticated, IsMember, IsAdmin)
    serializer_class = ChatInviteSerializer

    def get_queryset(self):
        return self.chat.invites.all()

    @property
    def get_serializer(self):
        if self.request.method == "POST":
            self.request.data["sender_id"] = self.request_member.id
            self.request.data["chat_id"] = self.chat.id
            return CreateChatInviteSerializer
        return ChatInviteSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=serializer.validated_data.get("target_id"))
        if self.chat.is_member(user):
            raise APIException("Пользователь уже есть в чате", status.HTTP_400_BAD_REQUEST)
        super(ChatInviteListApiView, self).perform_create(serializer)


class ChatInviteApiView(InviteMixin, UpdateAPIView, RetrieveAPIView, DestroyAPIView, APIView):
    permission_classes = (IsAuthenticated, IsMember, IsAdmin)
    serializer_class = ChatInviteSerializer

    def get_object(self):
        return self.invite

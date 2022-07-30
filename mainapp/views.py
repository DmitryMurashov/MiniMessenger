from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from mainapp.serializers import ChatMemberSerializer, ChatSerializer, MessageSerializer, ChatInviteSerializer
from mainapp.mixins import ChatMixin, ChatMemberMixin, MessageMixin, InviteMixin
from mainapp.permissions import IsMember, CanManageMessage, DeleteIfChatOwner, IsAdmin, ReadOnly
from authapp.models import User


class ChatListApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer

    def get(self, request):
        chats = [obj.chat for obj in request.user.chats.all()]
        serializer = self.serializer_class(chats, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        data = request.data.get("chat", {})
        data["owner_id"] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ChatApiView(ChatMemberMixin, APIView):
    permission_classes = (IsAuthenticated, DeleteIfChatOwner)
    serializer_class = ChatSerializer

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.chat)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, **kwargs):
        data = request.data.get("chat", {})
        serializer = self.serializer_class(instance=self.chat, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        self.chat.delete()
        return Response({}, status.HTTP_200_OK)


class ChatMessageListApiView(ChatMemberMixin, APIView):
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = MessageSerializer

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.chat.messages.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, **kwargs):
        data = request.data.get("message", {})
        data["author_id"] = self.member.id  # TODO: ??
        data["chat_id"] = self.chat.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ChatMessageApiView(MessageMixin, APIView):
    permission_classes = (IsAuthenticated, IsMember, CanManageMessage | ReadOnly)
    serializer_class = MessageSerializer

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.message)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, **kwargs):
        data = request.data.get("message", {})
        serializer = self.serializer_class(instance=self.message, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        self.message.delete()
        return Response({}, status.HTTP_200_OK)


class ChatMemberListApiView(ChatMixin, APIView):
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = ChatMemberSerializer

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.chat.members, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ChatMemberApiView(ChatMemberMixin, APIView):
    permission_classes = (IsAuthenticated, IsMember, IsAdmin | ReadOnly)
    serializer_class = ChatMemberSerializer

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.member)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, **kwargs):
        data = request.data.get("member")
        serializer = self.serializer_class(instance=self.member, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request):
        self.member.delete()
        return Response({}, status.HTTP_200_OK)


class ChatInviteListApiView(ChatMemberMixin, APIView):
    permission_classes = (IsAuthenticated, IsMember, IsAdmin)
    serializer_class = ChatInviteSerializer

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.chat.invites.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, **kwargs):
        data = request.data.get("invite")
        data["sender_id"] = self.member.id
        data["chat_id"] = self.chat.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        user = User.objects.get(id=serializer.validated_data.get("target_id"))
        if self.chat.is_member(user):
            return Response({"error": "Пользователь уже есть в чате"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ChatInviteApiView(InviteMixin, APIView):
    permission_classes = (IsAuthenticated, IsMember, IsAdmin)
    serializer_class = ChatInviteSerializer

    def get(self, request, **kwargs):
        serializer = self.serializer_class(self.invite)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        self.invite.delete()
        return Response({}, status.HTTP_200_OK)

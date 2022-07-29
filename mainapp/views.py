from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from mainapp.serializers import ChatMemberSerializer, ChatSerializer, MessageSerializer
from mainapp.mixins import ChatMixin, ChatMemberMixin, MessageMixin
from mainapp.permissions import IsMember, CanManageMessageOrReadOnly, DeleteIfChatOwner


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
    permission_classes = (IsAuthenticated, IsMember, CanManageMessageOrReadOnly)
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


class ChatMemberListApiView(ChatMixin, APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = ChatMemberSerializer

    def get(self, request, chat_id):
        serializer = self.serializer_class(self.chat.members, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ChatMemberApiView(ChatMemberMixin, APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = ChatMemberSerializer

    def get(self, request, chat_id):
        serializer = self.serializer_class(self.member)
        return Response(serializer.data, status.HTTP_200_OK)

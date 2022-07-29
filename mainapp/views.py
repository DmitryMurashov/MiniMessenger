from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from mainapp.serializers import ChatMemberSerializer, ChatSerializer, MessageSerializer
from mainapp.mixins import ChatMixin, MemberMixin
from mainapp.models import Message

from mainapp.permissions import IsMember


class ChatListApiView(APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer

    def get(self, request):
        chats = [obj.chat for obj in request.user.chats.all()]
        serializer = self.serializer_class(chats, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        data = request.data.get("chat", {})
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ChatApiView(MemberMixin, APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer

    def get(self, request, chat_id):
        serializer = self.serializer_class(self.chat)
        return Response(serializer.data, status.HTTP_200_OK)

    def update(self, request):
        data = request.data.get("chat", {})
        serializer = self.serializer_class(instance=self.chat, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request):
        if self.chat.owner == request.user or (self.member and self.member.is_admin):
            self.chat.delete()
            return Response({}, status.HTTP_200_OK)
        return Response({"error": "Для осуществления данного запроса пользователь должен быть владельцем или администратором чата"}, status.HTTP_403_FORBIDDEN)


class ChatMessageListApiView(ChatMixin, APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = MessageSerializer

    def get(self, request, chat_id):
        serializer = self.serializer_class(self.chat.messages.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ChatMessageApiView(ChatMixin, APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = MessageSerializer

    def get(self, request, chat_id, message_id):
        message = Message.objects.get(id=message_id)
        serializer = self.serializer_class(message)
        return Response(serializer.data, status.HTTP_200_OK)


class ChatMemberListApiView(ChatMixin, APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = ChatMemberSerializer

    def get(self, request, chat_id):
        serializer = self.serializer_class(self.chat.members, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ChatMemberApiView(MemberMixin, APIView):  # TODO: CRUD
    permission_classes = (IsAuthenticated, IsMember)
    serializer_class = ChatMemberSerializer

    def get(self, request, chat_id):
        serializer = self.serializer_class(self.member)
        return Response(serializer.data, status.HTTP_200_OK)

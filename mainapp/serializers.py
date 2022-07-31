from rest_framework import serializers
from mainapp.models import Chat, ChatMember, Message, ChatInvite
from authapp.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    is_private = serializers.BooleanField(default=True, required=False)
    name = serializers.CharField(max_length=50, required=False)
    image = serializers.ImageField(required=False)

    owner = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"
        depth = 2


class CreateChatSerializer(ChatSerializer):
    owner_id = serializers.IntegerField(write_only=True, required=True)


class ChatMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    chat = ChatSerializer(read_only=True)
    member_since = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChatMember
        fields = "__all__"
        depth = 2


class MessageSerializer(serializers.ModelSerializer):
    author = ChatMemberSerializer(read_only=True)
    chat = ChatSerializer(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        depth = 2


class CreateMessageSerializer(MessageSerializer):
    author_id = serializers.IntegerField(write_only=True, required=True)
    chat_id = serializers.IntegerField(write_only=True, required=True)


class ChatInviteSerializer(serializers.ModelSerializer):
    sender = ChatMemberSerializer(read_only=True)
    target = UserSerializer(read_only=True)
    chat = ChatSerializer(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChatInvite
        fields = "__all__"
        depth = 2


class CreateChatInviteSerializer(ChatInviteSerializer):
    sender_id = serializers.IntegerField(write_only=True, required=True)
    target_id = serializers.IntegerField(write_only=True, required=True)
    chat_id = serializers.IntegerField(write_only=True, required=True)

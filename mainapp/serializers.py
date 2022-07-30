from rest_framework import serializers
from mainapp.models import Chat, ChatMember, Message, ChatInvite
from authapp.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    owner_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Chat
        fields = "__all__"
        depth = 2


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

    author_id = serializers.IntegerField(write_only=True, required=False)
    chat_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = "__all__"
        depth = 2


class ChatInviteSerializer(serializers.ModelSerializer):
    sender = ChatMemberSerializer(read_only=True)
    target = UserSerializer(read_only=True)
    chat = ChatSerializer(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)

    sender_id = serializers.IntegerField(write_only=True)
    target_id = serializers.IntegerField(write_only=True)
    chat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ChatInvite
        fields = "__all__"
        depth = 2

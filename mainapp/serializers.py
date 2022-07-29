from rest_framework import serializers
from mainapp.models import Chat, ChatMember, Message
from authapp.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.IntegerField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"
        depth = 2


class ChatMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    chat = ChatSerializer()
    member_since = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChatMember
        fields = "__all__"
        depth = 2


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    chat = ChatSerializer()
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        depth = 2

from django.db import models
from authapp.models import User


class Chat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_chats')
    is_private = models.BooleanField(default=True)
    name = models.CharField(max_length=50, default="Chat")  # TODO: о умолчанию имя создателя
    image = models.ImageField(default="https://sun1-47.userapi.com/s/v1/if1/f-xqnN-x7i5-U-Kq3VRTt2h7m6dJT6K-XVVq0py6Yg9WOB2fhACUc3U3gOLbsbodwfzSwHbi.jpg?size=400x0&quality=96&crop=5,0,236,236&ava=1")
    created_at = models.DateTimeField(auto_now_add=True)

    def fetch_member(self, user: User, raise_exception: bool = True) -> 'ChatMember':
        try:
            return ChatMember.objects.get(user=user, chat=self)
        except ChatMember.DoesNotExist as NotFound:
            if raise_exception:
                raise NotFound

    def is_member(self, user: User) -> bool:
        return ChatMember.objects.filter(user=user, chat=self).exists()


class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='members')
    chat_custom_name = models.CharField(max_length=100, blank=True, null=True)
    member_since = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)


class Message(models.Model):
    author = models.ForeignKey(ChatMember, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(max_length=2000)
    sent_at = models.DateTimeField(auto_now_add=True)


class ChatInvite(models.Model):
    sender = models.ForeignKey(ChatMember, on_delete=models.CASCADE, related_name='sent_invites')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incoming_invites")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="invites")
    content = models.TextField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

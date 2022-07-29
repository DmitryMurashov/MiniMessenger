from django.db import models
from authapp.models import User
from typing import Union
from django.dispatch import receiver
from django.db.models.signals import post_save


class Chat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_chats')
    is_private = models.BooleanField(default=True)
    name = models.CharField(max_length=50, default="Chat")  # TODO: о умолчанию имя создателя
    image = models.ImageField(default="https://sun1-47.userapi.com/s/v1/if1/f-xqnN-x7i5-U-Kq3VRTt2h7m6dJT6K-XVVq0py6Yg9WOB2fhACUc3U3gOLbsbodwfzSwHbi.jpg?size=400x0&quality=96&crop=5,0,236,236&ava=1")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_member(self, user: User) -> Union[User, None]:
        try:
            return ChatMember.objects.get(user=user, chat=self)
        except ChatMember.DoesNotExist:
            return


class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='members')
    member_since = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    @receiver(post_save, sender=Chat)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ChatMember.objects.create(user=instance.owner, chat=instance, is_admin=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='all_messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(max_length=2000)
    sent_at = models.DateTimeField(auto_now_add=True)

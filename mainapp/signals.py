from utils.events import Event
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from mainapp.serializers import *
from mainapp.models import Chat, ChatMember, ChatInvite, Message


@receiver(post_save, sender=Chat, weak=False)
def on_user_create_chat(sender, instance, created, **kwargs):
    if created:
        ChatMember.objects.create(user=instance.owner, chat=instance, is_admin=True)


@receiver(post_save, sender=ChatInvite, weak=False)
def on_invite_accepted(sender, instance: ChatInvite, created, **kwargs):
    if not created:
        if instance.accepted:
            ChatMember.objects.create(user=instance.target, chat=instance.chat)
            instance.delete()


# Public events

@receiver(post_save, sender=Message, weak=False)
def on_message_event(sender, instance, created, **kwargs):
    if created:
        instance.chat.events.add(Event(
            event_type='on_message',
            instance=instance,
            serializer_class=MessageSerializer
        ))


@receiver(post_save, sender=ChatMember, weak=False)
def on_user_join_event(sender, instance, created, **kwargs):
    if created:
        instance.chat.events.add(Event(
            event_type='on_user_join',
            instance=instance,
            serializer_class=ChatMemberSerializer
        ))


@receiver(post_delete, sender=ChatMember, weak=False)
def on_user_leave_event(sender, instance, **kwargs):
    instance.chat.events.add(Event(
        event_type='on_user_join',
        instance=instance,
        serializer_class=ChatMemberSerializer
    ))

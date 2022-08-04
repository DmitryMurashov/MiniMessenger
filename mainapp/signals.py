from django.dispatch import receiver
from django.db.models.signals import post_save
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

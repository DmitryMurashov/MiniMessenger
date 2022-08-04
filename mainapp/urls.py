from django.urls import path
from mainapp import views as mainapp
app_name = 'mainapp'

urlpatterns = [
    path('chats/', mainapp.ChatListApiView.as_view(), name='chats'),
    path('chats/chat/<int:chat_id>/', mainapp.ChatApiView.as_view(), name='chat'),
    path('chats/chat/<int:chat_id>/events/<str:event_type>/', mainapp.ChatEventStreamApiView.as_view(), name='chat_events'),
    path('chats/chat/<int:chat_id>/messages/', mainapp.ChatMessageListApiView.as_view(), name='chat_messages'),
    path('chats/chat/<int:chat_id>/messages/message/<int:message_id>/', mainapp.ChatMessageApiView.as_view(), name='chat_message'),
    path('chats/chat/<int:chat_id>/members/', mainapp.ChatMemberListApiView.as_view(), name='chat_members'),
    path('chats/chat/<int:chat_id>/members/member/<int:member_id>/', mainapp.ChatMemberApiView.as_view(), name='chat_member'),
    path('chats/chat/<int:chat_id>/invites/', mainapp.ChatInviteListApiView.as_view(), name="invites"),
    path('chats/chat/<int:chat_id>/invites/invite/<int:invite_id>/', mainapp.ChatInviteApiView.as_view(), name="invite")
]

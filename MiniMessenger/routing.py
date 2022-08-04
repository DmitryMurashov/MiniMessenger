from django.urls import path, include
from channels.routing import URLRouter
from mainapp import routing


websocket_urlpatterns = [
    path('', URLRouter(routing.websocket_urlpatterns))
]

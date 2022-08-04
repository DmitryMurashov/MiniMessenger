import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from MiniMessenger import routing
from mainapp.middleware import JWTAuthenticationMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MiniMessenger.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthenticationMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

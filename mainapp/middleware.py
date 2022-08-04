from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from authapp.models import User
from authapp.backends import find_user


@database_sync_to_async
def get_user(token: str) -> User:
    return find_user(token)


class JWTAuthenticationMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        scope['user'] = None
        args = {arg.split("=")[0]:arg.split("=")[1] for arg in scope['query_string'].decode().split()}
        if token := args.get('token'):
            scope['user'] = await get_user(token)
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

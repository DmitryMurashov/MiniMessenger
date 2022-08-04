from rest_framework import authentication, exceptions
from django.conf import settings
import jwt
from authapp.models import User

authentication_header_prefix = 'JwtAuthToken'


def find_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Ошибка аутентификации: Срок действия токена истек')
    except jwt.exceptions.InvalidSignatureError:
        raise exceptions.AuthenticationFailed('Ошибка аутентификации: Ошибка проверки подписи')
    except Exception as UnknownError:
        raise exceptions.AuthenticationFailed('Ошибка аутентификации: Неизвестная ошибка') from UnknownError

    try:
        user = User.objects.get(pk=payload['id'])
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('Пользователь соответствующий данному токену не найден')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('Данный пользователь деактивирован')

    return user


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != authentication_header_prefix.lower():
            return None

        return find_user(token), token

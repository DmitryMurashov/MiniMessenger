from rest_framework import authentication, exceptions
from django.conf import settings
import jwt
from authapp.models import User
from traceback import format_exception


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'JwtAuthToken'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Ошибка аутентификации: Срок действия токена истек')
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('Ошибка аутентификации: Ошибка проверки подписи')
        except Exception as UnknownError:
            print("".join(format_exception(type(UnknownError), UnknownError, UnknownError.__traceback__)))
            raise exceptions.AuthenticationFailed('Ошибка аутентификации: Неизвестная ошибка')

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь соответствующий данному токену не найден')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Данный пользователь деактивирован')

        return user, token

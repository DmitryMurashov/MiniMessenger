from django.http import HttpRequest
from rest_framework.views import Response, Request
from rest_framework.views import APIView, status
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ObjectMixin(APIView):
    class NotImplementedError(Exception):
        pass

    def __return_response(self, request, response,*args, **kwargs):
        self.headers = self.default_response_headers
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def get_mixin_object(self, request: Request, *args, **kwargs) -> None:
        raise self.NotImplementedError("Object must have this method implemented")

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        initialized_request = super(ObjectMixin, self).initialize_request(request)
        try:
            self.get_mixin_object(initialized_request, *args, **kwargs)
        except ObjectDoesNotExist:
            response = Response({"detail": "Object not found"}, status.HTTP_404_NOT_FOUND)
            return self.__return_response(initialized_request, response, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

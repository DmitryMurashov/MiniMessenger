from django.http import HttpRequest
from rest_framework.views import Response, Request
from rest_framework.views import APIView, status
from django.core.exceptions import ObjectDoesNotExist


class ObjectMixin(APIView):
    def __init__(self):
        super(ObjectMixin, self).__init__()
        self.args = None
        self.kwargs = None
        self.request = None
        self.headers = None
        self.response = None

    class NotImplementedError(Exception):
        pass

    def get_mixin_object(self, request: Request, *args, **kwargs) -> None:
        raise self.NotImplementedError("Object must have this method implemented")

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            self.get_mixin_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            response = Response({"detail": "Object not found"}, status.HTTP_404_NOT_FOUND)
            return self.finalize_response(request, response, *args, **kwargs)

        try:
            self.initial(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

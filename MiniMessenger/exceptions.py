from rest_framework.views import exception_handler
from rest_framework.views import Response, status
from utils.functions import get_traceback_text
from rest_framework.exceptions import NotFound

FAIL_TEXT_COLOR = '\033[91m'


def __DoesNotExistsErrorHandler(error, context):
    return exception_handler(NotFound(f"Object not found: {error}"), context)


def core_exception_handler(exception, context):
    if response := __handle_generic_error(exception, context):
        return response
    rest_response = exception_handler(exception, context)
    if rest_response is not None:
        return rest_response
    print(FAIL_TEXT_COLOR + get_traceback_text(exception))
    return Response({"error": "Unknown internal server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


def __handle_generic_error(exception, context):
    handlers = {
        'DoesNotExist': __DoesNotExistsErrorHandler
    }
    exception_class_name = exception.__class__.__name__
    if exception_class_name in handlers:
        return handlers[exception_class_name](exception, context)

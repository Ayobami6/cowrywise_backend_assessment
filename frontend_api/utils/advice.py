

from functools import wraps
from sparky_utils.response import service_response
from .exceptions import ServiceException
from sparky_utils.exceptions import handle_internal_server_exception
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


def exception_advice(func):
    """Exception advice for all endpoint http verbs handler

    Args:
        func (handler method): http method handler

    Returns:
        func: returns decorated handler method
    """    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ServiceException):
                return service_response(status="error", message=e.message, status_code=e.status_code)
            elif isinstance(e, ValidationError):
                return service_response(status="error", message=e.message, status_code=400)
            elif isinstance(e, ObjectDoesNotExist):
                return service_response(status="error", message=str(e), status_code=404)
            else:
                return handle_internal_server_exception()
    return wrapper
                    
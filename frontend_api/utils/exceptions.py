from functools import wraps
from sparky_utils.response import service_response
from sparky_utils.exceptions import handle_internal_server_exception


class ServiceException(Exception):
    """Custom service exception class to except validation errors and other service exceptions
    """    
    def __init__(self, message, status_code):
        super().__init__()
        self.message = message
        self.status_code = status_code
        

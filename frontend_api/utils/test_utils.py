import pytest
from .exceptions import ServiceException

def test_service_exception_returns_right_message():
    # get an instance of service exception
    exception = ServiceException(message="Not Found", status_code=404)
    assert exception.status_code == 404
    assert exception.message == "Not Found"
    assert isinstance(exception, Exception)
    
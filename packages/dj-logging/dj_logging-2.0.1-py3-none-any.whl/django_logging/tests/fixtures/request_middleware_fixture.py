from typing import Callable

import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from django_logging.middleware import RequestLogMiddleware


@pytest.fixture
def request_factory() -> RequestFactory:
    """
    Fixture to create a RequestFactory instance for generating request objects.

    Returns:
    -------
    RequestFactory
        An instance of RequestFactory for creating mock requests.
    """
    return RequestFactory()


@pytest.fixture
def get_response() -> Callable:
    """
    Fixture to create a mock get_response function.

    Returns:
    -------
    function
        A function that returns an HttpResponse with a dummy response.
    """

    def _get_response(request: RequestFactory) -> HttpResponse:
        return HttpResponse("Test Response")

    return _get_response


@pytest.fixture
def request_middleware() -> RequestLogMiddleware:
    """
    Fixture to create an instance of RequestLogMiddleware.

    Returns:
    -------
    RequestLogMiddleware
        An instance of RequestLogMiddleware with the sample HttpResponse.
    """
    middleware = RequestLogMiddleware(lambda request: HttpResponse("OK"))
    middleware.log_sql = True

    return middleware

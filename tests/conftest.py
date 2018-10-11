# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--test_url", action="store",
        required=True, help="Test URL to test"
    )
    parser.addoption(
        "--web_server_host", action="store",
        required=True, help="host of the webserver"
    )
    parser.addoption(
        "--web_server_port", action="store",
        required=True, help="port of the webserver"
    )


@pytest.fixture
def test_url(request):
    return request.config.getoption("--test_url")


@pytest.fixture
def web_server_port(request):
    return request.config.getoption("--web_server_port")


@pytest.fixture
def web_server_host(request):
    return request.config.getoption("--web_server_host")

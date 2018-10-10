# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--web_server_port", action="store",
        default="5000", help="port of the webserver"
    )
    parser.addoption(
        "--web_server_host", action="store",
        default="localhost", help="host of the webserver"
    )


@pytest.fixture
def web_server_port(request):
    return request.config.getoption("--web_server_port")


@pytest.fixture
def web_server_host(request):
    return request.config.getoption("--web_server_host")

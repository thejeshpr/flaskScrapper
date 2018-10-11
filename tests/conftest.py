"""
This is configuration for pytest to enable custom tweaks
"""
import pytest


def pytest_addoption(parser):
    """
    Add custom command line params
    """
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
    """
    Make test_url avaiable as pytest config
    """
    return request.config.getoption("--test_url")


@pytest.fixture
def web_server_port(request):
    """
    Make web_server_port avaiable as pytest config
    """
    return request.config.getoption("--web_server_port")


@pytest.fixture
def web_server_host(request):
    """
    Make web_server_host avaiable as pytest config
    """
    return request.config.getoption("--web_server_host")

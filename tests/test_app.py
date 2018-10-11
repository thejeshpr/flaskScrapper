import pytest
import requests
from urllib.parse import urljoin


PROXIES = {
    "http": "",
    "https": "",
}


def http_get(url, params=None):
    return requests.get(url, params=params, proxies=PROXIES)


class TestApp(object):
    """ PyTest tests fot flaskScrapper"""

    TEST_CONFIG = None
    web_server_url = None
    test_url = None

    @classmethod
    def setup_class(cls):
        """
        Setup Test Parameters
        """
        port = pytest.config.getoption('web_server_port')
        host = pytest.config.getoption('web_server_host')
        cls.test_url = pytest.config.getoption('test_url')
        cls.web_server_url = 'http://{}:{}'.format(host, port)

    def test_indexpage(self):
        """
        Test the Index Page
        """
        print(TestApp.web_server_url)
        response = http_get(TestApp.web_server_url)
        assert 'Simple Web Scrapper' in response.text

    def test_parseValidURLUsingHTML(self):
        """
        Test with Valid URL
        """
        qp = {
            "url": TestApp.test_url
        }
        response = http_get(
            urljoin(TestApp.web_server_url, 'parse'), params=qp)
        assert '<p class="lead"><strong>Status Code :</strong>200</p>'\
               in response.text

    def test_parseWrongURLUsingHTML(self):
        """
        Test with Invalid URL
        """
        qp = {
            "url": 'http://wqragvdb362v8ndjjruj.dndun.dhr/fjjr'
        }
        response = http_get(
            urljoin(TestApp.web_server_url, 'parse'), params=qp)
        assert ('Unable to parse given url, status code : 404'
                in response.text)

    def test_parseValidURLUsingAPI(self):
        """
        Test with Valid URL using API
        """
        qp = {
            "url": TestApp.test_url,
            "returnJson": "true"
        }
        response = http_get(
            urljoin(TestApp.web_server_url, 'parse'), params=qp)
        assert response.json()['status'] == "Success"

    def test_parseInvalidURLUsingAPI(self):
        """
        Test with Invalid URL using API
        """
        qp = {
            "url": 'http://wqragvdb362v8ndjjruj.dndun.dhr/fjjr',
            "returnJson": "true"
        }
        response = http_get(
            urljoin(TestApp.web_server_url, 'parse'), params=qp)
        assert response.json()['status'] == "Failed"

    @classmethod
    def teardown_class(cls):
        pass

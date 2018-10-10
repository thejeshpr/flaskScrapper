import json
import os
import requests
from urllib.parse import urljoin


WEB_APP_HOST = os.getenv("WEB_APP_HOST") or "localhost"
WEB_APP_PORT = os.getenv("WEB_APP_PORT") or "5000"
URL = 'http://{}:{}'.format(WEB_APP_HOST, WEB_APP_PORT)
PROXIES = {
          "http": "",
          "https": "",
        }


def http_get(url, params=None):
    return requests.get(url, params=params, proxies=PROXIES)


class TestApp(object):
    """ PyTest tests fot flaskScrapper"""

    TEST_CONFIG = None

    @classmethod
    def setup_class(cls):
        """
        Reads test config from test_config.json
        """
        with open('test_config.json', 'r') as fd:
            cls.TEST_CONFIG = json.load(fd)

    def test_indexpage(self):
        """
        Test the Index Page
        """
        response = http_get(URL)
        assert 'Simple Web Scrapper' in response.text

    def test_parseValidURLUsingHTML(self):
        """
        Test with Valid URL
        """
        qp = {
            "url": TestApp.TEST_CONFIG['ValidURL']
        }
        response = http_get(urljoin(URL, 'parse'), params=qp)
        print(response.text)
        assert '<p class="lead"><strong>Status Code :</strong>200</p>' \
               in response.text

    def test_parseWrongURLUsingHTML(self):
        """
        Test with Invalid URL
        """
        qp = {
            "url": TestApp.TEST_CONFIG['InvalidURL']
        }
        response = http_get(urljoin(URL, 'parse'), params=qp)
        assert ('Unable to open given url, please verify the url and try'
                ' again!!' in response.text)

    def test_parseValidURLUsingAPI(self):
        """
        Test with Valid URL using API
        """
        qp = {
            "url": TestApp.TEST_CONFIG['ValidURL'],
            "returnJson": "true"
        }
        response = http_get(urljoin(URL, 'parse'), params=qp)
        assert response.json()['status'] == "Success"

    def test_parseInvalidURLUsingAPI(self):
        """
        Test with Invalid URL using API
        """
        qp = {
            "url": TestApp.TEST_CONFIG['InvalidURL'],
            "returnJson": "true"
        }
        response = http_get(urljoin(URL, 'parse'), params=qp)
        assert response.json()['status'] == "Failed"

    @classmethod
    def teardown_class(cls):
        pass

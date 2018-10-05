import json
from bs4 import BeautifulSoup
from flask import request
import requests
from urllib.parse import urlparse, parse_qs


DEFAULT_URL_PROTOCOL = "https://"
URL_QP_NAME = 'url'
RETURN_JSON_QP_NAME = 'returnJson'


def read_tags_def():
    """
    Reads and return tags def from tagsDefinition from JSON tagsDefinition.json
    Return : tagsDefinition
    """
    with open('tagsDefinition.json', 'r') as fd:
        tags_def = json.load(fd)
    return tags_def


def get_clean_text(text):
    """
    Clean text content : replace \\n \\t and remove blank spaces
    Return : clean text if text else None
    """
    if type(text) is str:
        return " ".join(
                    text.replace("\r", "").replace("\n", "").strip().split()
                    )
    else:
        return text


def validate_url(url):
    """
    Validates the given url and adds if protocol missing
    Returns : url, scheme, netloc, path and query_parms
    """
    url_parser = urlparse(url)
    if not url_parser.scheme:
        url = DEFAULT_URL_PROTOCOL + url
        url_parser = urlparse(url)
    return (
        url,
        url_parser.scheme,
        url_parser.netloc,
        url_parser.path,
        parse_qs(url_parser.query)
    )


def convert_data_to_json_frmt(parsed_data):
    """
    Convert the given data to json suitable output
    Returns : Dict
    """
    return {
        "ParsedResult": parsed_data['context'],
        "Title": parsed_data['title'],
        "URL": parsed_data['title'],
        "return_json": True
    }


def parse_url(url):
    """
    Parse the given url and return the specific tags
    Return : Tags, Title, Error
    """
    return_data = {}

    try:
        response = requests.get(url)
    except Exception as e:
        return {
            "error": ("Unable to open given url"
                      ", please verify the url and try again!!"
                     )
        }
    else:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            tags_def = read_tags_def()
            for tag_def in tags_def:
                found_tags = []
                for elm in soup.find_all(tag_def["name"]):
                    elm_info = {}
                    if tag_def['find_text']:
                        elm_info['text'] = get_clean_text(elm.text)
                    for attr in tag_def['attrs']:
                        elm_info[attr] = elm.get(attr)
                    found_tags.append(elm_info)
                return_data[tag_def["name"]] = found_tags

            return {
                "context": return_data,
                "title": get_clean_text(soup.find("title").text)
            }
        else:
            return {
                "error": "Unable to parse given url, status code : {}".
                         format(response.status_code)
            }


def process_request():
    """
    Process the requests
    Return : Processed Data
    """
    url = request.args.get(URL_QP_NAME)

    # validate the given url in the request and extract url info
    url, scheme, netloc, path, query_param = validate_url(url)

    # Parse the url
    parsed_data = parse_url(url)
    parsed_data['url'] = url
    if request.args.get(RETURN_JSON_QP_NAME) == 'true':
        return convert_data_to_json_frmt(parsed_data)
    return parsed_data

from bs4 import BeautifulSoup
from flask import request
import requests
from urllib.parse import urlparse, parse_qs


DEFAUL_URL_PROTOCOL = "https://"

FIND_ONLY_ATTRS = {
    "a" : ["href"],
    "img" : ["src", "height", "width"]
}

NON_TEXT_TAGS = [
    "img",
]

HEADINGS     = ["h1", "h2", "h3", "h4", "h5", "h6"]
OTHER_TAGS   = ['a', 'p', 'img']
TAGS_QP_NAMES = ["tag-a", "tag-p", "tag-img", "tag-h"]
URL_QP_NAME = 'url'


def get_clean_text(text):
    """
    Clean text content : replace \\n \\t and remove blank spaces
    Return : clean text if text else None
    """    
    if type(text) is str:
        return " ".join(text.replace("\r", "").replace("\n","").strip().split())
    else : return text


def validate_url(url):
    """
    Validates the given url and adds if protocol missing
    Returns : url, scheme, netloc, path and query_parms
    """
    url_parser = urlparse(url)    
    if not url_parser.scheme:
        url = DEFAUL_URL_PROTOCOL + url
        url_parser = urlparse(url)
    return (
        url,
        url_parser.scheme,
        url_parser.netloc,
        url_parser.path,
        parse_qs(url_parser.query)
    )


def parse_url(url, tags_to_parse):
    """
    Parse the given url and return the specific tags
    Return : Tags, Title, Error
    """
    return_data = {}

    try:
        response = requests.get(url)
    except Exception as e:
        return (
            None,
            None,
            "Unable to open given url, please verify the url and try again!!"
        )
    else:    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in tags_to_parse:
                tags_found = []         
                for elm in soup.find_all(tag):                    
                    elm_info = {}
                    
                    if tag in FIND_ONLY_ATTRS:
                        for attr in FIND_ONLY_ATTRS[tag]:
                            elm_info[attr] = elm.get(attr)
                    if tag not in NON_TEXT_TAGS:
                        elm_info['text'] = get_clean_text(elm.text)

                    tags_found.append(elm_info)
                     
                return_data[tag] = tags_found

            return (
                return_data,
                get_clean_text(soup.find("title").text),
                None
            )
    
        else:
            return (
                None,
                None, 
                {
                    "status_code" : response.status_code,
                    "error_message" : "Unable to parse given url"
                }
            )


def process_request():
    """
    Process the requests
    Return : 
    """
    # get all QPs which is not null
    tags_to_extract = [ request.args.get(qp_name) \
                        for qp_name in TAGS_QP_NAMES[:3] \
                        if request.args.get(qp_name) ]

    # check if heading tag is set and then append all headins
    headings_qp = request.args.get(TAGS_QP_NAMES[-1])
    if headings_qp == "h":
        tags_to_extract = tags_to_extract + HEADINGS

    # get url qp value
    url = request.args.get(URL_QP_NAME)

    # if tags to extract is empty, use default tags to extract
    tags_to_extract = tags_to_extract if tags_to_extract else HEADINGS + OTHER_TAGS

    # validat the given url in the request and extract url info    
    url, scheme, netloc, path, query_param = validate_url(url)

    # parse given url and find specified tags
    context, title, err = parse_url(url, tags_to_extract)

    return context, title, err, url
from urllib.parse import urlparse, parse_qs


DEFAUL_URL_PROTOCOL = "https://"

def get_clean_text(text):
    """
    Clean text content : replace \\n \\t and remove blank spaces
    Return : clean text if text else None
    """
    #print("-------------", type(text))    
    if type(text) is str:
        return " ".join(text.replace("\r", "").replace("\n","").strip().split())
    else : return text

def validate_url(url):
    """
    Validates the given url and adds if protocol missing
    Returns : url, scheme, netloc, path and query_parms
    """
    url_parser = urlparse(url)
    print("SCHEME", url_parser.scheme)
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
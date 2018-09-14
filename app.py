from flask import Flask, render_template, request
import os
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse, parse_qs
#import socket

from customLib import (
    get_clean_text,
    validate_url
    )

# Connect to Redis
#redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

FIND_ONLY_ATTRS = {
    "a" : ["href"],
    "img" : ["src", "height", "width"]
}

NON_TEXT_TAGS = [
    "img",
]



"""def validate_url(url):
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
    )"""


def parse_url(url, tags_to_parse):
    print("URL---------------->", url)
    return_data = {}

    try:
        response = requests.get(url)
    except Exception as e:
        return None, None, "Unable to open given url, please verify the url and try again!!"
    else:    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in tags_to_parse:
                tags_found = []         
                for elm in soup.find_all(tag):
                    #print(elm, "---------",elm.attrs)
                    #break
                    """attr = elm.attrs
                    attr['text'] = get_clean_text(elm.text)
                    """
                    elm_info = {}
                    
                    if tag in FIND_ONLY_ATTRS:
                        for attr in FIND_ONLY_ATTRS[tag]:
                            elm_info[attr] = elm.get(attr)
                    if tag not in NON_TEXT_TAGS:
                        elm_info['text'] = get_clean_text(elm.text)

                    tags_found.append(elm_info)

                    """return_data.append({
                    "tag" : tag,
                    "findings" : tags_found
                    })"""
                #return_data.append({tag : tags_found}) 
                return_data[tag] = tags_found

            return return_data, get_clean_text(soup.find("title").text), None
    
        else:
            return None, None, {
                "status_code" : response.status_code,
                "error_message" : "Unable to parse given url"
            }

@app.route("/")
def index():
    context = ""
    return render_template('index.html', context=context)

@app.route("/parse")
def parse():
    """
    Parse the given url and return specific tags
    Return : Index template with parsed data
    """
    #return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)
    headings = ["h1", "h2", "h3", "h4", "h5", "h6"]
    default_tags = ['a', 'p', 'img'] + headings
    extra_qry_parms = ["tag-a", "tag-p", "tag-img"]
    tags_to_extract = [request.args.get(qry_parm_name) for qry_parm_name in extra_qry_parms if request.args.get(qry_parm_name)]

    headings_qp = request.args.get("tag-h")
    if headings_qp == "h":
        tags_to_extract = tags_to_extract + headings
    #print(tags_to_extract)    
    
    tags_to_extract = tags_to_extract if tags_to_extract else default_tags

    url = request.args.get('url')
    a = request.args.get("tag-a")
    p = request.args.get("tag-p")
    img = request.args.get("tag-img")
    h = request.args.get("tag-h")
    #print(json.dumps(request.args, indent=4))

    #pprint(parse_url(url, tags_to_extract))

    #pprint(validate_url(url))
    
    url, scheme, netloc, path, query_param = validate_url(url)

    context = {
        "url" : url,
        "p" : p,
        "img" : img,
        "h" : h
    }
    print("URL---->", url, tags_to_extract)
    context, title, err = parse_url(url, tags_to_extract)
    pprint(context)
    if err:
        return render_template('index.html', error=err)
    return render_template('index.html', 
        context=json.dumps(context, indent=4),
        url=url,
        title=title
        )

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
from flask import Flask, render_template, request
import os
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
#from urllib.parse import urlparse, parse_qs
#import socket

from customLib import (
    get_clean_text,
    validate_url,
    parse_url,
    process_request
    )

# Connect to Redis
#redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/")
def index():
    """
    Index of the website
    Return : renders index.html
    """
    context = ""
    return render_template('index.html', context=context)


@app.route("/parse")
def parse():
    """
    Parse the given url and return specific tags
    Return : renders index.html
    """
    #return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

    context, title, err, url = process_request()
    #pprint(context)
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
from flask import Flask, render_template, request, jsonify
import os
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
#from urllib.parse import urlparse, parse_qs
#import socket

TITLE = "MyTinyWebScrapper"

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
    return render_template('index.html', context=context, title=TITLE)


@app.route("/parse")
def parse():
    """
    Parse the given url and return specific tags
    Return : renders index.html
    """
    #return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)
    
    parsed_data = process_request()

    if parsed_data.get('error'):
        return render_template('index.html',
            error=parsed_data['error'],
            url=parsed_data.get('url'),
            title=TITLE
            )

    # Check if JSON response requsted
    if parsed_data['return_json'] == True:
        # delete return_json from parsed_data, since its required by enduser
        del(parsed_data['return_json'])
        return jsonify(parsed_data)

    return render_template('index.html', 
        context=json.dumps(parsed_data['context'], indent=4),
        url=parsed_data['url'],
        web_page_title=parsed_data['title'],
        title=TITLE
        )

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
from flask import Flask, render_template, jsonify
import os
import json
from customLib import process_request
# import socket

TITLE = os.getenv("WEB_APP_NAME") or "TinyWebScrapper"

# Connect to Redis
# redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

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
    # return html.format(name=os.getenv("NAME", "world")
    # , hostname=socket.gethostname(), visits=visits)

    parsed_data = process_request()

    # Check if JSON response requsted
    if parsed_data.get('return_json'):
        # delete return_json from parsed_data, since its required by enduser
        del(parsed_data['return_json'])
        return jsonify(parsed_data)

    if parsed_data.get('error') is not None:
        return render_template('index.html',
                               error=parsed_data['error'],
                               url=parsed_data.get('url'),
                               title=TITLE)

    return render_template('index.html',
                           context=json.dumps(
                                              parsed_data['context'],
                                              indent=4),
                           url=parsed_data['url'],
                           web_page_title=parsed_data['title'],
                           title=TITLE)


if __name__ == "__main__":
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port=80)

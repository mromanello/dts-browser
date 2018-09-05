import json
import sys

from flask import render_template, request, current_app
from urllib.request import build_opener

from app import app_bp


if sys.version_info < (3, 6):
    json_loads = lambda s: json_loads(s.decode("utf-8")) if isinstance(s, bytes) else json.loads(s)
else:
    json_loads = json.loads


def query_json_endpoint(url, method='GET', headers_arg=None):
    headers = {'Content-Type': 'application/ld+json'}
    if headers_arg is not None:
        headers.update(headers_arg)

    if method == 'GET':
        op = build_opener()
        op.addheaders = [(k, v) for k, v in headers.items()]
        data = op.open(url, timeout=15).read()
    else:
        raise NotImplementedError

    return json_loads(data)


def query_nautilus(request, endpoint):
    base_url = current_app.config["NAUTILUS_URL"]
    endpoint_url = current_app.config["NAUTILUS_%s_ENDPOINT" % endpoint.upper()]
    params = ""
    if len(request.args) > 0:
        params = "?" + "&".join(["%s=%s" % (k, v) for k, v in request.args.items()])
    url = base_url + endpoint_url + params
    return url, query_json_endpoint(url)


"""
    ROUTES
"""


@app_bp.route("/")
def index():
    return render_template("main/index.html")


@app_bp.route("/collections")
def collections():
    api_url, collection = query_nautilus(request, "collections")
    return render_template("main/collection.html", collection=collection, api_url=api_url)


@app_bp.route("/navigation")
def navigation():
    return render_template("main/navigation.html")


@app_bp.route("/document")
def document():
    return render_template("main/document.html")

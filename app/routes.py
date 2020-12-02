import os

import json
import sys
import lxml.etree as ET
import pprint
from flask import render_template, request, current_app, Markup
from urllib.request import build_opener
from urllib.parse import urljoin

from app import app_bp


if sys.version_info < (3, 6):
    json_loads = (
        lambda s: json_loads(s.decode("utf-8"))
        if isinstance(s, bytes)
        else json.loads(s)
    )
else:
    json_loads = json.loads


def query_endpoint(url, method="GET", headers_arg=None):
    headers = {"Content-Type": "application/ld+json", "User-Agent": "DTS Client"}
    if headers_arg is not None:
        headers.update(headers_arg)

    if method == "GET":
        op = build_opener()
        op.addheaders = [(k, v) for k, v in headers.items()]
        data = op.open(url, timeout=15).read()
    else:
        raise NotImplementedError

    return data


def query_dts_api(args, endpoint):
    base_url = args["baseurl"]
    entrypoints = json.loads(query_endpoint(base_url))
    _args = [(k, v) for k, v in args.items() if k != "baseurl"]
    params = ""
    if len(_args) > 0:
        params = "?" + "&".join(["%s=%s" % (k, v) for k, v in _args])

    # patch for betamasaheft, as the document endpoint is called
    # "document" (instead of "documents" as per spec)
    if endpoint == "documents":
        if "documents" not in entrypoints:
            endpoint = "document"
    url = urljoin(base_url, entrypoints[endpoint]) + params
    return url, query_endpoint(url)


def query_aggregator(args, endpoint):
    base_url = current_app.config["AGGREGATOR_URL"]
    endpoint_url = current_app.config["AGGREGATOR_%s_ENDPOINT" % endpoint.upper()]
    params = ""
    if len(args) > 0:
        params = "?" + "&".join(
            ["%s=%s" % (k, v) for k, v in args.items() if k != "baseurl"]
        )
    url = base_url + endpoint_url + params
    return url, query_endpoint(url)


xslt = ET.parse(os.getcwd() + "/app/static/xsl/tei2html.xsl")
transform = ET.XSLT(xslt)

"""
ROUTES
"""


@app_bp.route("/")
def index():
    return render_template("main/index.html")


@app_bp.route("/entrypoints")
def entrypoints():
    api_url, collection = query_aggregator(request.args, "collections")
    collection = json_loads(collection)
    return render_template(
        "main/collection.html", collection=collection, api_url=api_url
    )


@app_bp.route("/collections")
def collections():
    base_url = request.args["baseurl"]
    api_url, collection = query_dts_api(request.args, "collections")
    collection = json_loads(collection)
    return render_template(
        "main/collection.html",
        collection=collection,
        api_url=api_url,
        base_url=base_url,
    )


@app_bp.route("/document")
def document():

    # document
    document_api_url, doc = query_dts_api(request.args, "documents")
    print(f"document_api_url {document_api_url}")
    dom = ET.fromstring(doc)
    newdom = transform(dom)
    center_div = newdom.xpath("//*[name()='div' and @id='center']")[0]
    safe_dom = Markup(ET.tostring(center_div).decode("utf-8"))

    # navigation
    navigation_args = {"id": request.args["id"], "baseurl": request.args["baseurl"]}
    navigation_api_url, navigation = query_dts_api(navigation_args, "navigation")
    navigation = json_loads(navigation)

    return render_template(
        "main/document.html",
        navigation=navigation,
        document=safe_dom,
        navigation_api_url=navigation_api_url,
        document_api_url=document_api_url,
    )

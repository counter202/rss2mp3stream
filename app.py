import os
import requests
import xml.etree.ElementTree as ET
from flask import Flask, Response, jsonify, request, redirect

DEFAULT_FEED_URL = "https://api.dr.dk/podcasts/v1/feeds/hemmeligheder-2"

app = Flask(__name__)

def fetch_rss_text(url: str) -> str:
    r = requests.get(
        url,
        headers={
            "User-Agent": "dr-rss-proxy/1.0",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.text

def get_first_enclosure(xml_text: str) -> str:
    root = ET.fromstring(xml_text)

    channel = root.find("channel")
    if channel is None:
        return ""

    first_item = channel.find("item")
    if first_item is None:
        return ""

    enclosure = first_item.find("enclosure")
    if enclosure is None:
        return ""

    return enclosure.attrib.get("url", "")

@app.get("/")
def health():
    return jsonify(
        service="dr rss proxy",
        endpoints=[
            "/rss",
            "/rss?format=streamlatest",
            "/rss?url=...&format=streamlatest"
        ],
        default_feed=DEFAULT_FEED_URL,
    )

@app.get("/rss")
def rss():
    url = request.args.get("url") or DEFAULT_FEED_URL
    format_type = request.args.get("format")

    xml_text = fetch_rss_text(url)

    if format_type == "streamlatest":
        enclosure_url = get_first_enclosure(xml_text)

        if not enclosure_url:
            return Response("No enclosure found", status=404)

        return redirect(enclosure_url, code=302)

    return Response(xml_text, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)

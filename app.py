import os
import requests
from flask import Flask, Response, jsonify, request

FEED_URL = "https://api.dr.dk/podcasts/v1/feeds/hemmeligheder-2"

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

@app.get("/")
def health():
    return jsonify(
        service="dr rss proxy",
        endpoints=["/rss", "/rss?url=..."],
        default_feed=FEED_URL,
    )

@app.get("/rss")
def rss():
    url = request.args.get("url") or FEED_URL
    xml_text = fetch_rss_text(url)
    return Response(xml_text, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)

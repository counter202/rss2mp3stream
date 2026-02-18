import requests

FEED_URL = "https://api.dr.dk/podcasts/v1/feeds/hemmeligheder-2"

def fetch_rss(url: str) -> str:
    r = requests.get(
        url,
        headers={
            "User-Agent": "rss-fetcher/1.0",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.text

def main() -> None:
    rss_xml = fetch_rss(FEED_URL)
    print(rss_xml)

if __name__ == "__main__":
    main()

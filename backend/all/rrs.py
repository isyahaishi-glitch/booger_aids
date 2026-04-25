import feedparser
import requests
import re
from datetime import datetime
from URL import FEEDS
import time
from flask import Flask,jsonify
from flask_cors import CORS
import re
from html import unescape

app = Flask(__name__)
CORS(app)
seen_links = set()
KEYWORDS: list =[""]
INTERVAL: int = 60  
def safe_parse(url):
    """Fetch and sanitize RSS feed before parsing to avoid XML token errors"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # Remove invalid XML characters
        content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', response.text)
        return feedparser.parse(content)
    except Exception as e:
        print(f" Failed to fetch {url}: {e}")
        return None

# ANTARA RSS Feed URLs
def fetch_feed(name: str, url: str, count: int = 1) -> list[dict]:
    """Fetch and display articles from an RSS feed"""
    print(f"\n{name.upper()}")
        
    feed = safe_parse(url)
    if feed is None or feed.bozo:
        exc = getattr(feed, "bozo_exception", "Unknown error") if feed else "No feed data"
        print(f" Error parsing feed: {exc}")
        return []

        
    seen = set()
    for entry in feed.entries[:count]:
        link = entry.get("link", "")
        if link in seen:
            continue          
        seen.add(link)
        
    if feed is None or feed.bozo:
        exc = getattr(feed, "bozo_exception", "Unknown error") if feed else "No feed data"
        print(f" Error parsing feed: {exc}")
        return []
    
    articles = []
    for i, entry in enumerate(feed.entries[:count], 1):
        published = entry.get("published", "N/A")
        title     = entry.get("title", "No title")
        link      = entry.get("link", "")
        summary = clean_summary(entry.get("summary", ""))
        articles.append({
            "title"    : title,
            "link"     : link,
            "published": published,
            "summary"  : summary,

        })
    return articles

def clean_summary(raw: str, max_len: int = 150) -> str:
    text = re.sub(r'<[^>]+>', '', raw)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len] + "..." if len(text) > max_len else text

def keyword_filter(articles: list[dict], keywords: list[str]) -> list[dict]:
    matched = []
    for article in articles:
        text = (article["title"] + " " + article["summary"]).lower()
        for kw in keywords:
            if kw.lower() in text:
                article["matched_keyword"] = kw
                matched.append(article)
                break
    return matched

@app.route("/antara")
def route_antara():
    all_articles = []
    for name, url in FEEDS.items():
        all_articles.extend(fetch_feed(name, url, count=1))
    return jsonify(all_articles)

@app.route("/filter-antara")
def route_filter_antara():
    """Return only keyword-matched articles as JSON."""
    all_articles = []
    for name, url in FEEDS.items():
        all_articles.extend(fetch_feed(name, url, count=1))
    matched = keyword_filter(all_articles, KEYWORDS)
    return jsonify(matched)

def run_polling():
    global seen_links
    while True:
        try:
            all_articles = []
            for name, url in FEEDS.items():
                all_articles.extend(fetch_feed(name, url, count=1))

            new_articles = [a for a in all_articles if a["link"] not in seen_links]

            ts = datetime.now().strftime("%H:%M:%S")
            if new_articles:
                matched = keyword_filter(new_articles, KEYWORDS)
                print(f"\n[{ts}] 🆕 {len(new_articles)} new article(s) found")
                print("=" * 60)

                if matched:
                    for a in matched:
                        print(f" [{a['matched_keyword'].upper()}] {a['title']}")
                        print(f"   {a['link']}\n")
                else:
                    print("No new articles matched the keywords.")

                for a in new_articles:
                    seen_links.add(a["link"])
            else:
                print(f"\n[{ts}] No new articles found.")

        except Exception as e:
            print(f" Error: {e}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

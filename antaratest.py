import feedparser
import requests
import re
from datetime import datetime

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
        print(f"❌ Failed to fetch {url}: {e}")
        return None

# ANTARA RSS Feed URLs
FEEDS = {
    "Terkini"      : "https://www.antaranews.com/rss/terkini.xml",
    "Top News"     : "https://www.antaranews.com/rss/top-news.xml",
    "Politik"      : "https://www.antaranews.com/rss/politik.xml",
    "Hukum"        : "https://www.antaranews.com/rss/hukum.xml",
    "Ekonomi"      : "https://www.antaranews.com/rss/ekonomi.xml",
    "Bisnis"       : "https://www.antaranews.com/rss/ekonomi-bisnis.xml",
    "Metro"        : "https://www.antaranews.com/rss/metro.xml",
    "Kriminalitas" : "https://www.antaranews.com/rss/metro-kriminalitas.xml",
    "Jabar"        : "https://jabar.antaranews.com/rss/terkini.xml",
}

def fetch_feed(name, url, count=5):
    """Fetch and display articles from an RSS feed"""
    print(f"\n📰 ANTARA - {name.upper()}")
    print("=" * 60)
    
    feed = safe_parse(url)
    
    if feed is None or feed.bozo:
        print(f"❌ Error parsing feed: {feed.bozo_exception}")
        return []
    
    articles = []
    for i, entry in enumerate(feed.entries[:count], 1):
        published = entry.get("published", "N/A")
        title     = entry.get("title", "No title")
        link      = entry.get("link", "")
        summary   = entry.get("summary", "")[:100] + "..."
        
        print(f"{i}. {title}")
        print(f"   🕐 {published}")
        print(f"   🔗 {link}")
        print(f"   📝 {summary}")
        print()
        
        articles.append({
            "title"    : title,
            "link"     : link,
            "published": published,
            "summary"  : summary,
            "source"   : f"ANTARA - {name}"
        })
    
    return articles

def keyword_filter(articles, keywords):
    """Simple keyword filter for OSINT relevance"""
    matched = []
    for article in articles:
        text = (article["title"] + " " + article["summary"]).lower()
        for kw in keywords:
            if kw.lower() in text:
                article["matched_keyword"] = kw
                matched.append(article)
                break
    return matched

if __name__ == "__main__":
    all_articles = []
    
    # Fetch terkini and nasional feeds
    for name, url in list(FEEDS.items())[:3]:
        articles = fetch_feed(name, url, count=5)
        all_articles.extend(articles)
    
    # Test keyword filter
    KEYWORDS = ["gempa", "banjir", "korupsi", "hacker", "siber", "teknologi", "AI"]
    
    print("\n" + "=" * 60)
    print("🔍 KEYWORD FILTER RESULTS")
    print(f"   Keywords: {KEYWORDS}")
    print("=" * 60)
    
    matched = keyword_filter(all_articles, KEYWORDS)
    
    if matched:
        for a in matched:
            print(f"✅ [{a['matched_keyword'].upper()}] {a['title']}")
            print(f"   {a['link']}\n")
    else:
        print("No articles matched the keywords.")
    
    print(f"\n📊 Total fetched: {len(all_articles)} | Matched: {len(matched)}")
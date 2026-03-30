import feedparser
import requests
import re

# BBC RSS Feed URLs
FEEDS = {
    "Top Stories"  : "https://feeds.bbci.co.uk/news/rss.xml",
    "World"        : "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Asia"         : "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "Technology"   : "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "Science"      : "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "Business"     : "https://feeds.bbci.co.uk/news/business/rss.xml",
    "Health"       : "https://feeds.bbci.co.uk/news/health/rss.xml",
}

def safe_parse(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', response.text)
        return feedparser.parse(content)
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None

def fetch_feed(name, url, count=10):
    print(f"\n🌍 BBC - {name.upper()}")
    print("=" * 60)

    feed = safe_parse(url)

    if feed is None:
        return []

    if feed.bozo and not feed.entries:
        print(f"❌ Error parsing feed: {feed.bozo_exception}")
        return []

    articles = []
    for i, entry in enumerate(feed.entries[:count], 1):
        published = entry.get("published", "N/A")
        title     = entry.get("title", "No title")
        link      = entry.get("link", "")
        summary   = entry.get("summary", "")[:120] + "..."

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
            "source"   : f"BBC - {name}"
        })

    return articles

def keyword_filter(articles, keywords):
    """Empty list = show all"""
    if not keywords:
        return articles
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

    # Fetch first 3 feeds
    for name, url in list(FEEDS.items())[:4]:
        articles = fetch_feed(name, url, count=5)
        all_articles.extend(articles)

    # Keywords — [] = show all
    KEYWORDS = []

    print("\n" + "=" * 60)
    print("🔍 FILTER RESULTS")
    print(f"   Keywords: {'ALL (no filter)' if not KEYWORDS else KEYWORDS}")
    print("=" * 60)

    matched = keyword_filter(all_articles, KEYWORDS)

    if matched:
        for a in matched:
            kw = a.get("matched_keyword", "ALL")
            print(f"✅ [{kw.upper()}] {a['title']}")
            print(f"   🔗 {a['link']}\n")
    else:
        print("No articles found.")

    print(f"\n📊 Total fetched: {len(all_articles)} | Showing: {len(matched)}")
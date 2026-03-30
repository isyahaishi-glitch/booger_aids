import feedparser
import json
from datetime import datetime
import requests


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




def fetch_bmkg_earthquake():
    """Fetch latest earthquake data from BMKG"""
    url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        gempa = data["Infogempa"]["gempa"]
        
        print("=" * 50)
        print("🌍 BMKG - GEMPA TERKINI")
        print("=" * 50)
        print(f"📅 Tanggal  : {gempa['Tanggal']}")
        print(f"🕐 Jam      : {gempa['Jam']}")
        print(f"📍 Wilayah  : {gempa['Wilayah']}")
        print(f"💥 Magnitudo: {gempa['Magnitude']}")
        print(f"📏 Kedalaman: {gempa['Kedalaman']}")
        print(f"🌐 Koordinat: {gempa['Lintang']}, {gempa['Bujur']}")
        print(f"⚠️  Potensi  : {gempa['Potensi']}")
        print("=" * 50)
        
        return gempa
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching BMKG data: {e}")
        return None

def fetch_bmkg_recent(count=5):
    """Fetch last N earthquakes from BMKG"""
    url = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        gempa_list = data["Infogempa"]["gempa"][:count]
        
        print(f"\n📋 {count} GEMPA TERAKHIR:")
        print("=" * 50)
        for i, g in enumerate(gempa_list, 1):
            print(f"{i}. [{g['Tanggal']} {g['Jam']}] M{g['Magnitude']} - {g['Wilayah']}")
        print("=" * 50)
        
        return gempa_list
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    fetch_bmkg_earthquake()   # Latest single earthquake
    fetch_bmkg_recent(5)      # Last 5 earthquakes



# ANTARA RSS Feed URLs tinggal 

def fetch_feed(name, url, count=5):
    """Fetch and display articles from an RSS feed"""
    print(f"\n📰 ANTARA - {name.upper()}")
    print("=" * 60)
    
    feed = feedparser.parse(url)
    
    if feed.bozo:
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
    
    # Test keyword filter/// 
    KEYWORDS = [
        # "gempa", "banjir", "korupsi", "hacker", "siber", "teknologi", "AI"
        ]
    
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
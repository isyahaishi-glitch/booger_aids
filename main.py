import feedparser
import json
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
urlbmkg = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
urlbmkg2 = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
ANTARA_TERKINI = "https://www.antaranews.com/rss/terkini.xml"
GEMINI_API_KEY = GEMINI_API_KEY 
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"

FEEDS = {
                        # ANTARA NEWS
    # "Terkini"      : "https://www.antaranews.com/rss/terkini.xml",
    # "Top News"     : "https://www.antaranews.com/rss/top-news.xml",
    # "Politik"      : "https://www.antaranews.com/rss/politik.xml",
    # "Hukum"        : "https://www.antaranews.com/rss/hukum.xml",
    # "Ekonomi"      : "https://www.antaranews.com/rss/ekonomi.xml",
    # "Bisnis"       : "https://www.antaranews.com/rss/ekonomi-bisnis.xml",
    # "Metro"        : "https://www.antaranews.com/rss/metro.xml",
    # "Kriminalitas" : "https://www.antaranews.com/rss/metro-kriminalitas.xml",
    # "Jabar"        : "https://jabar.antaranews.com/rss/terkini.xml",

                        # BBC
    "Top Stories"  : "https://feeds.bbci.co.uk/news/rss.xml",
    "World"        : "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Asia"         : "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "Technology"   : "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "Science"      : "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "Business"     : "https://feeds.bbci.co.uk/news/business/rss.xml",
    "Health"       : "https://feeds.bbci.co.uk/news/health/rss.xml",
}



def fetch_bmkg_earthquake():
    """Fetch latest earthquake data from BMKG"""
    # url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
    
    try:
        response = requests.get(urlbmkg, timeout=10)
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
    # url = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
    
    try:
        response = requests.get(urlbmkg2, timeout=10)
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





# ANTARA RSS Feed URLs 

def fetch_feed(name, url, count=5):
    """Fetch and display articles from an RSS feed"""
    print(f"\n📰  {name.upper()}")
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
    if not keywords:  # ← if empty, return everything
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

def analyze_with_ai(article):
    # Move the persona to a system instruction if possible, 
    # but for a simple POST request, we'll keep it in the prompt.
    prompt = f"""Extract OSINT from this Indonesian news:
Title: {article['title']}
Summary: {article['summary']}

Return JSON with keys: location, location_type, category, entities, keywords, severity, summary_en."""

    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            # This is the "Magic Bullet" for JSON errors:
            "response_mime_type": "application/json",
        }
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        result = response.json()

        # The model will now return a CLEAN string of JSON
        raw = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        return json.loads(raw)

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None

def print_osint_report(article, analysis):
    # print("\n" + "=" * 60)
    # print("🔍 OSINT INTELLIGENCE REPORT")
    # print("=" * 60)
    print(f"📰 Title     : {article['title']}")
    print(f"🔗 Link      : {article['link']}")
    print(f"🕐 Published : {article['published']}")
    print(f"📡 Source    : {article['source']}")
    print()
    if analysis:
        print(f"📍 Location  : {analysis.get('location', 'N/A')} ({analysis.get('location_type', '')})")
        print(f"🏷️  Category  : {analysis.get('category', 'N/A')}")
        print(f"⚠️  Severity  : {analysis.get('severity', 'N/A')}")
        print(f"🔑 Keywords  : {', '.join(analysis.get('keywords', []))}")
        print(f"👥 Entities  : {', '.join(analysis.get('entities', []))}")
        print(f"🌐 Summary   : {analysis.get('summary_en', 'N/A')}")
    else:
        print("❌ AI analysis unavailable")
    print("=" * 60)
if __name__ == "__main__":

    fetch_bmkg_earthquake()   # Latest single earthquake
    fetch_bmkg_recent(5)      # Last 5 earthquakes


    all_articles = []
    
    # Fetch terkini and nasional feeds
    for name, url in FEEDS.items():
        articles = fetch_feed(name, url, count=1)
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
            kw = a.get('matched_keyword', 'ALL')
            print(f"✅ [{kw.upper()}] {a['title']}")
            print(f"   {a['link']}\n")
    else:
        print("No articles matched the keywords.")
    
    print(f"\n📊 Total fetched: {len(all_articles)} | Matched: {len(matched)}")
    article = fetch_feed(name, url, count=1)[0]  

    if not article:
        print("❌ No article fetched.")
        exit()
    
    analysis = analyze_with_ai(article)
    print_osint_report(article, analysis)
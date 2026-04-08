import feedparser
import requests
import re
import json
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ── Config ──────────────────────────────────────────────

ANTARA_TERKINI = "https://www.antaranews.com/rss/terkini.xml"
GEMINI_API_KEY = GEMINI_API_KEY 
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
SEVERITY_RUBRIC = """
- CRITICAL: Active data breaches, ransomware on government/infrastructure, or national security threats.
- HIGH: Significant corruption, large-scale financial fraud, or major cyber attacks on private companies.
- MEDIUM: Legal cases, regional protests, minor data leaks, or policy changes affecting security.
- LOW: General news, routine arrests, planned maintenance, or sports/entertainment.
"""
# ────────────────────────────────────────────────────────

def safe_parse(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', response.text)
        return feedparser.parse(content)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print(f"❌ Failed to fetch feed: {e}")
        return None

def fetch_single_article():
    """Fetch just 1 latest article from ANTARA"""
    feed = safe_parse(ANTARA_TERKINI)
    if not feed or not feed.entries:
        return None
    entry = feed.entries[0]
    return {
        "title"    : entry.get("title", ""),
        "summary"  : entry.get("summary", ""),
        "link"     : entry.get("link", ""),
        "published": entry.get("published", ""),
        "source"   : "ANTARA - Terkini"
    }

def analyze_with_ai(article):
    # Move the persona to a system instruction if possible, 
    # but for a simple POST request, we'll keep it in the prompt.
    prompt = f"""
        Act as an OSINT Analyst. Rate the severity of this Indonesian news:
        
        Title: {article['title']}
        Summary: {article['summary']}

        Use these rules for 'severity':
        {SEVERITY_RUBRIC}

        Return JSON with key: severity
        """

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
        # print(f"📍 Location  : {analysis.get('location', 'N/A')} ({analysis.get('location_type', '')})")
        # print(f"🏷️  Category  : {analysis.get('category', 'N/A')}")
        print(f"⚠️  Severity  : {analysis.get('severity', 'N/A')}")
    #     print(f"🔑 Keywords  : {', '.join(analysis.get('keywords', []))}")
    #     print(f"👥 Entities  : {', '.join(analysis.get('entities', []))}")
    #     print(f"🌐 Summary   : {analysis.get('summary_en', 'N/A')}")
    # else:
        print("❌ AI analysis unavailable")
    print("=" * 60)

if __name__ == "__main__":
    print("📡 Fetching latest article from ANTARA...")
    article = fetch_single_article()

    if not article:
        print("❌ No article fetched.")
        exit()

    print(f"✅ Got: {article['title']}")
    print("🤖 Sending to Gemini for analysis...")

    analysis = analyze_with_ai(article)
    print_osint_report(article, analysis)
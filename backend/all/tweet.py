import asyncio
from playwright.async_api import async_playwright
import json
from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from flask_cors import CORS
import threading
from URL import USERNAMES

app = Flask(__name__)
CORS(app)
load_dotenv()

auth_token1 = os.getenv("auth_token")
ct01 = os.getenv("ct0")

COOKIES = [
    {"name": "auth_token", "value": auth_token1, "domain": ".x.com", "path": "/"},
    {"name": "ct0",        "value": ct01,        "domain": ".x.com", "path": "/"},
]

# USERNAMES = ["Bloomberg", "Reuters", "CNN"]

# global so Flask can access it
results = []

async def scrape():
    global results
    temp = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.add_cookies(COOKIES)
        page = await context.new_page()

        for username in USERNAMES:
            try:
                await page.goto(f"https://x.com/{username}",
                    wait_until="domcontentloaded",
                    timeout=60000)

                await page.wait_for_selector("article", timeout=15000)
                await asyncio.sleep(3)

                tweet = await page.query_selector("article")

                if tweet:
                    text = await tweet.inner_text()

                    images = []
                    imgs = await tweet.query_selector_all("img")
                    for img in imgs:
                        src = await img.get_attribute("src")
                        if src and "pbs.twimg.com/media" in src:
                            images.append(src)

                    temp.append({
                        "source": username,
                        "text": text,
                        "created_at": "",
                        "image_url": images[0] if images else None
                    })

            except Exception as e:
                print(f"Error scraping {username}: {e}")
                continue

            await asyncio.sleep(5)

        await browser.close()

    results = temp
    print(json.dumps(results, indent=2))

def run_scraper():
    asyncio.run(scrape())

@app.route("/tweets")
def route_tweets():
    return jsonify(results)

if __name__ == "__main__":
    # run scraper in background thread
    thread = threading.Thread(target=run_scraper)
    thread.daemon = True
    thread.start()

    # start Flask
    app.run(debug=False, port=5000)
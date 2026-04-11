import requests

HEADERS = {"User-Agent": "military-tracker/1.0"}

# Test different dist values
for dist in [100, 200, 250, 300, 400, 500]:
    res = requests.get(
        f"https://opendata.adsb.fi/api/v3/lat/-6.2/lon/106.8/dist/{dist}",
        headers=HEADERS, timeout=10
    )
    print(f"dist={dist} → HTTP {res.status_code} — {len(res.json().get('ac', [])) if res.status_code == 200 else 'ERR'} aircraft")
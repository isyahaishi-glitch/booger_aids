from flask import Flask,jsonify
import requests
import time
from datetime import datetime
from flask_cors import CORS
from filter import MIL_CALLSIGN_PATTERNS,MIL_HEX_RANGES,MISSION_TYPE_MAP,AIRCRAFT_TYPE_MAP,MISSION_COLORS,CIVILIAN_PREFIXES,MIL_HEX_EXACT,TILES,HEADERS
app = Flask(__name__)
CORS(app)

FILTER_ENABLED = True
def classify_mission_type(ac):

    callsign = str(ac.get("flight", "")).strip().upper()
    ac_type  = str(ac.get("t") or ac.get("type") or "").strip().upper()
 

    best_match, best_len = None, 0
    for prefix, mtype in MISSION_TYPE_MAP.items():
        if callsign.startswith(prefix) and len(prefix) > best_len:
            best_match, best_len = mtype, len(prefix)
    if best_match:
        return best_match
 

    for type_key, mtype in AIRCRAFT_TYPE_MAP.items():
        if ac_type.startswith(type_key) or type_key in ac_type:
            return mtype
 

    reasons_text = " ".join(ac.get("reasons", [])).upper()
    if any(k in reasons_text for k in ("TNI", "INDONESIAN", "USAF", "US MILITARY", "UK MILITARY", "FRENCH", "AUSTRALIAN")):
        return "Transport"
 
    return "Unknown"
 
def is_civilian(ac):
    callsign = str(ac.get("flight", "")).strip().upper()
    reg      = str(ac.get("r", "")).strip().upper()  

    for prefix in CIVILIAN_PREFIXES:
        if callsign.startswith(prefix):
            return True

    if reg.startswith("N") and reg[1:].replace("-", "").isalnum():
        return True

    return False
def check_military(ac):
    if is_civilian(ac):      
        return []
    callsign = str(ac.get("flight", "")).strip().upper()
    hex_code = str(ac.get("hex", "")).strip().lower()
    reasons = []

    for pattern in MIL_CALLSIGN_PATTERNS:
        if callsign.startswith(pattern):
            reasons.append(f"callsign prefix '{pattern}'")
            break

    try:
        hex_int = int(hex_code, 16)
        for start, end, label in MIL_HEX_RANGES:
            if start <= hex_int <= end:
                reasons.append(f"hex range → {label}")
                break
    except ValueError:
        pass

    if hex_code in MIL_HEX_EXACT:
        reasons.append(f"known hex → {MIL_HEX_EXACT[hex_code]}")

    if not callsign:
        alt = ac.get("alt_baro", 0) or 0
        gs  = ac.get("gs", 0) or 0
        if isinstance(alt, int) and alt > 20000 and gs > 250:
            reasons.append("no callsign, high alt+speed (possible military/state)")

    return reasons

def fetch_tiles(lat, lon,dist, label):
    url = f"https://opendata.adsb.fi/api/v3/lat/{lat}/lon/{lon}/dist/{dist}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code != 200:
            print(f" Failed to fetch data: HTTP {res.status_code} - restrying 15 sec")
            return []
        return res.json().get("ac", [])
    except Exception as e:
        print(f"    {label} → {e}")
        return []
    

@app.route("/plane") 
def get_aircraft():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    seen_hex = set()   # deduplicate across tiles
    hits     = []
    total    = 0

    for lat, lon, dist, label in TILES:
        aircraft_list = fetch_tiles(lat, lon, dist, label)
        total += len(aircraft_list)

        for ac in aircraft_list:
            hex_code = ac.get("hex", "")
            if hex_code in seen_hex:
                continue
            seen_hex.add(hex_code)
            if FILTER_ENABLED:
                reasons = check_military(ac)
                if reasons:
                    hits.append({
    "callsign": str(ac.get("flight", "")).strip() or None,
    "hex": ac.get("hex"),
    "lat": ac.get("lat"),
    "lon": ac.get("lon"),
    "altitude": ac.get("alt_baro"),
    "speed": ac.get("gs"),
    "type": ac.get("type"),
    "squawk": ac.get("squawk"),
    "tile": label,
    "reasons": reasons,
    "mission_type": classify_mission_type(ac),
    "is_military": FILTER_ENABLED and bool(reasons)
})
            else:
                hits.append({
    "callsign": str(ac.get("flight", "")).strip() or None,
    "hex": ac.get("hex"),
    "lat": ac.get("lat"),
    "lon": ac.get("lon"),
    "altitude": ac.get("alt_baro"),
    "speed": ac.get("gs"),
    "type": ac.get("type"),
    "squawk": ac.get("squawk"),
    "tile": label,
    "reasons": [" filter disabled — showing all"],
    "mission_type": classify_mission_type(ac),
    "is_military": False
    
})

    # print(f"    Scanned ~{total} aircraft ({len(seen_hex)} unique) — {len(hits)} flagged")
    # print("─" * 80)
    for hit in hits:
        callsign = hit.get("callsign") or "(no callsign)"
        alt = hit.get("altitude") or "?"
        gs = hit.get("speed") or "?"
        ac_type = hit.get("type") or "?"
        squawk = hit.get("squawk") or "?"
        lat = hit.get("lat")
        lon = hit.get("lon")
        lat_str = f"{lat:.2f}" if isinstance(lat, float) else "?"
        lon_str = f"{lon:.2f}" if isinstance(lon, float) else "?"
        tile_label = hit.get("tile") or "?"
        reasons = hit.get("reasons") or []

        print(
            f"  ✈  {callsign:<12} hex={hit.get('hex'):<8} type={ac_type:<6} "
            f"alt={str(alt):<6} gs={str(gs):<5} squawk={squawk:<6} "
            f"lat={lat_str} lon={lon_str} [{tile_label}]"
            f"\n       → {', '.join(reasons)}"
        )

    mode = "ALL AIRCRAFT (filter OFF)" if not FILTER_ENABLED else "military filter ON"
    print(f"\n[{ts}]  Scanning {len(TILES)} tiles — mode: {mode}")
    return jsonify({"timestamp": ts, "count": len(hits), "data": hits})
if __name__ == "__main__":
    app.run(debug=True, port=5003)
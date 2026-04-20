from flask import Flask,jsonify
import requests
import time
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Known Indonesian + regional military callsign prefixes
MIL_CALLSIGN_PATTERNS = [

    # --- USA ---
    "RCH",     # USAF Air Mobility Command (Reach)
    "MC",      # Military Command generic
    "AF",      # US Air Force generic
    "NAVY",    # US Navy
    "MARINE",  # US Marine Corps
    "VM",      # USMC aviation (VMFA, etc.)
    "HOIST",   # SAR / rescue helos
    "PAT",     # Patrol aircraft
    "SPAR",    # US govt VIP (often used by USAF)
    "SAM",     # Special Air Mission (VIP)
    "VENUS",   # USAF VIP transport
    "REACH",   # Full callsign version
    "HAWK",    # Often fighters/interceptors
    "EAGLE",   # Fighters (F-15 etc.)
    "VIPER",   # F-16 callsign
    "RAPTOR",  # F-22
    "TEXACO",  # Tanker aircraft
    "SHELL",   # Tanker
    "AR",      # Aerial refueling shorthand

    # --- NATO / Europe ---
    "NATO",    # NATO ops
    "OTAN",    # NATO (French)
    "RRR",     # RAF transport (Royal Air Force)
    "ASCOT",   # UK military transport
    "COTAM",   # French Air Force transport
    "FAF",     # French Air Force
    "GAF",     # German Air Force (Luftwaffe)
    "LUFTHANSA", # Sometimes used for military charter
    "BAF",     # Belgian Air Force
    "DAF",     # Danish Air Force
    "RNLAF",   # Netherlands AF
    "SWAF",    # Swedish Air Force

    # --- Asia-Pacific ---
    "TNI",     # Indonesia (general)
    "TNIAU",   # Indonesian Air Force
    "TNIAD",   # Indonesian Army aviation
    "TNIAL",   # Indonesian Navy aviation
    "CASA",    # Indonesian CN-235
    "PAKSA",   # Presidential escort
    "VVIP",    # VIP flights

    "RMAF",    # Malaysia
    "PTM",     # Malaysia military
    "RSAF",    # Singapore
    "RTAF",    # Thailand
    "PAF",     # Philippines
    "JASDF",   # Japan Air Self-Defense Force
    "JMSDF",   # Japan Maritime Self-Defense Force
    "ROKAF",   # South Korea Air Force
    "PLAAF",   # China Air Force
    "PLAN",    # China Navy aviation

    # --- Australia / NZ ---
    "RAAF",    # Royal Australian Air Force
    "RNZAF",   # Royal New Zealand Air Force

    # --- Middle East ---
    "UAEAF",   # UAE Air Force
    "QAF",     # Qatar Air Force
    "RSAF_SA", # Saudi Air Force
    "IAF",     # Israeli Air Force

    # --- Russia / Eastern ---
    "VVS",     # Russian Air Force
    "RF",      # Russian Federation aircraft
    "RFF",     # Russian military flights

    # --- Generic military patterns ---
    "MIL",     # Generic military
    "ARMY",    # Army aviation
    "AIRFORCE",
    "NAVAL",
    "DEFENSE",
]
# Indonesian military ICAO hex blocks (TNI-AU assigned ranges)
# Format: (start_hex, end_hex, label)
MIL_HEX_RANGES = [
    (0x8A0000, 0x8A7FFF, "TNI-AU (Indonesian Military)"),  # narrowed
    (0xADF000, 0xAFFFFF, "USAF"),                          # actual USAF block
    (0xAE0000, 0xAEFFFF, "US Military"),                   # actual US mil block
    (0x43C000, 0x43CFFF, "UK Military"),
    (0x3B0000, 0x3BFFFF, "French Military"),
    (0x687000, 0x6873FF, "Australian Military (RAAF)"),
]
MISSION_TYPE_MAP = {
    # ISR
    "ISR": "ISR", "JSTARS": "ISR", "RIVET": "ISR", "COBRA": "ISR",
    "DRAGON": "ISR", "SHADOW": "ISR", "REAPER": "ISR", "PRED": "ISR",
    "PAT": "ISR", "HOIST": "ISR",
 
    # VIP
    "SAM": "VIP", "SPAR": "VIP", "VENUS": "VIP",
    "PAKSA": "VIP", "VVIP": "VIP",
 
    # Bomber
    "DOOM": "Bomber", "HAVOC": "Bomber", "BONE": "Bomber",
    "SPIRIT": "Bomber", "BUFF": "Bomber",
 
    # Command & Control
    "MC": "Command", "NAVY": "Command", "BRASS": "Command", "GOLF": "Command",
    "MARINE": "Command",
 
    # Tanker
    "TEXACO": "Tanker", "SHELL": "Tanker", "AR": "Tanker", "KC": "Tanker",
 
    # Transport / Airlift
    "RCH": "Transport", "REACH": "Transport", "ATLAS": "Transport",
    "ASCOT": "Transport", "COTAM": "Transport",
    "TNI": "Transport", "TNIAU": "Transport", "TNIAD": "Transport", "TNIAL": "Transport",
    "AF": "Transport", "RMAF": "Transport", "RSAF": "Transport",
    "RTAF": "Transport", "PAF": "Transport", "RAAF": "Transport", "RNZAF": "Transport",
    "JASDF": "Transport", "JMSDF": "Transport", "ROKAF": "Transport",
 
    # Fighter
    "HAWK": "Fighter", "EAGLE": "Fighter", "VIPER": "Fighter",
    "RAPTOR": "Fighter", "TALON": "Fighter",
}
 
# 2. Aircraft ICAO type code → mission type
AIRCRAFT_TYPE_MAP = {
    # ISR / Recon
    "E3":    "ISR",
    "E8":    "ISR",
    "RC135": "ISR",
    "U2":    "ISR",
    "P3":    "ISR",
    "P8":    "ISR",
    "EP3":   "ISR",
    "RQ4":   "ISR",
    "MQ9":   "ISR",
    "MQ1":   "ISR",
    # VIP
    "VC25":  "VIP",
    "C32":   "VIP",
    "C37":   "VIP",
    "C40":   "VIP",
    "E4":    "VIP",
    # Command
    "E6":    "Command",
    # Bomber
    "B52":   "Bomber",
    "B1":    "Bomber",
    "B2":    "Bomber",
    "TU95":  "Bomber",
    "TU22":  "Bomber",
    # Tanker
    "KC135": "Tanker",
    "KC10":  "Tanker",
    "KC46":  "Tanker",
    "IL78":  "Tanker",
    # Transport
    "C17":   "Transport",
    "C130":  "Transport",
    "C5":    "Transport",
    "C295":  "Transport",
    "CN235": "Transport",
    "C27":   "Transport",
    "AN12":  "Transport",
    "AN26":  "Transport",
    "IL76":  "Transport",
    # Fighter
    "F15":   "Fighter",
    "F16":   "Fighter",
    "F22":   "Fighter",
    "F35":   "Fighter",
    "F18":   "Fighter",
    "FA18":  "Fighter",
    "SU27":  "Fighter",
    "SU30":  "Fighter",
    "MIG29": "Fighter",
    "JAS39": "Fighter",
}
 
MISSION_COLORS = {
    "ISR":       "#ef4444",
    "VIP":       "#a855f7",
    "Bomber":    "#f97316",
    "Command":   "#ec4899",
    "Tanker":    "#eab308",
    "Transport": "#3b82f6",
    "Fighter":   "#06b6d4",
    "Unknown":   "#6b7280",
}
 
CIVILIAN_PREFIXES = [
    # Indonesian civilian airlines
    "BTK",  # Batik Air
    "CTV",  # Citilink
    "GIA",  # Garuda Indonesia
    "AWQ",  # Air Asia Indonesia
    "SJV",  # Sriwijaya Air
    "LNI",  # Lion Air
    "IDX",  # Indonesia AirAsia Extra
    "WIN",  # Wings Air
    "TGN",  # Trigana Air
    # US civilian
    "UAL",  # United Airlines
    "AAL",  # American Airlines
    "DAL",  # Delta
    "SWA",  # Southwest
    "UPS",  # UPS
    "FDX",  # FedEx
    "N",    # US civil registration (N-numbers) — catch all
]
# Known specific military hex codes (add as you discover them)
MIL_HEX_EXACT = {
    "ae1234": "USAF Special",
    # add more as observed
}
TILES = [
    # SE Asia (existing)
    (-6.2,  106.8, 250, "Java / Jakarta"),
    ( 1.0,  110.0, 250, "Borneo"),
    (-2.5,  120.0, 250, "Sulawesi"),
    (-5.0,  130.0, 250, "Maluku"),
    (-4.0,  140.0, 250, "Papua"),
    ( 5.0,  103.0, 250, "Malacca Strait"),
    ( 8.0,  112.0, 250, "South China Sea"),
    (-20.0, 130.0, 250, "Northern Australia"),
    ( 15.0, 108.0, 250, "Vietnam / Philippines"),
    ( 25.0, 121.0, 250, "Taiwan / East China Sea"),
    ( 35.0, 127.0, 250, "Korea / Japan"),

    # Middle East (new)
    ( 24.0,  54.0, 250, "UAE / Oman Gulf"),
    ( 26.0,  50.0, 250, "Persian Gulf / Bahrain"),
    ( 24.0,  45.0, 250, "Saudi Arabia"),
    ( 33.0,  44.0, 250, "Iraq / Syria"),
    ( 32.0,  35.0, 250, "Israel / Lebanon"),
    ( 15.0,  44.0, 250, "Yemen"),
    ( 29.0,  34.0, 250, "Sinai / Red Sea"),
    ( 37.0,  39.0, 250, "Turkey / Eastern Med"),
]
HEADERS = {"User-Agent": "military-tracker/1.0"}

# on/pareman filter
FILTER_ENABLED = True
def classify_mission_type(ac):
    """
    Priority order:
      1. Callsign prefix  (longest match wins)
      2. Aircraft type code (t or type field)
      3. Hex-range label inside reasons[]
      4. "Unknown"
    """
    callsign = str(ac.get("flight", "")).strip().upper()
    ac_type  = str(ac.get("t") or ac.get("type") or "").strip().upper()
 
    # 1. Callsign — longest prefix wins to avoid "MC" swallowing "MARINE"
    best_match, best_len = None, 0
    for prefix, mtype in MISSION_TYPE_MAP.items():
        if callsign.startswith(prefix) and len(prefix) > best_len:
            best_match, best_len = mtype, len(prefix)
    if best_match:
        return best_match
 
    # 2. Aircraft type code
    for type_key, mtype in AIRCRAFT_TYPE_MAP.items():
        if ac_type.startswith(type_key) or type_key in ac_type:
            return mtype
 
    # 3. Infer from hex-range label already in reasons list
    reasons_text = " ".join(ac.get("reasons", [])).upper()
    if any(k in reasons_text for k in ("TNI", "INDONESIAN", "USAF", "US MILITARY", "UK MILITARY", "FRENCH", "AUSTRALIAN")):
        return "Transport"
 
    return "Unknown"
 
def is_civilian(ac):
    callsign = str(ac.get("flight", "")).strip().upper()
    reg      = str(ac.get("r", "")).strip().upper()  # registration field

    for prefix in CIVILIAN_PREFIXES:
        if callsign.startswith(prefix):
            return True

    # N-number registration = US civilian
    if reg.startswith("N") and reg[1:].replace("-", "").isalnum():
        return True

    return False
def check_military(ac):
    if is_civilian(ac):      # ← add this at the top
        return []
    callsign = str(ac.get("flight", "")).strip().upper()
    hex_code = str(ac.get("hex", "")).strip().lower()
    reasons = []

    # 1. Callsign prefix match (word-boundary aware)
    for pattern in MIL_CALLSIGN_PATTERNS:
        if callsign.startswith(pattern):
            reasons.append(f"callsign prefix '{pattern}'")
            break

    # 2. Hex range match
    try:
        hex_int = int(hex_code, 16)
        for start, end, label in MIL_HEX_RANGES:
            if start <= hex_int <= end:
                reasons.append(f"hex range → {label}")
                break
    except ValueError:
        pass

    # 3. Exact hex match
    if hex_code in MIL_HEX_EXACT:
        reasons.append(f"known hex → {MIL_HEX_EXACT[hex_code]}")

    # 4. No callsign + unusual altitude/speed combo (ghost aircraft)
    if not callsign:
        alt = ac.get("alt_baro", 0) or 0
        gs  = ac.get("gs", 0) or 0
        if isinstance(alt, int) and alt > 20000 and gs > 250:
            reasons.append("no callsign, high alt+speed (possible military/state)")

    return reasons

# --- Main ---
def fetch_tiles(lat, lon,dist, label):
    url = f"https://opendata.adsb.fi/api/v3/lat/{lat}/lon/{lon}/dist/{dist}"
    try:

        
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code != 200:
            print(f"⚠️ Failed to fetch data: HTTP {res.status_code} - restrying 15 sec")
            return []
        return res.json().get("ac", [])
    except Exception as e:
        print(f"  ⚠️  {label} → {e}")
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
    "reasons": ["⚠️ filter disabled — showing all"],
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
    print(f"\n[{ts}] 🔍 Scanning {len(TILES)} tiles — mode: {mode}")
    return jsonify({"timestamp": ts, "count": len(hits), "data": hits})
if __name__ == "__main__":
    app.run(debug=True, port=5003)
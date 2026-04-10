import requests
import time
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
    (0x8A0000, 0x8AFFFF, "TNI-AU (Indonesian Military)"),
    (0xADF000, 0xAFFFFF, "USAF"),
    (0xAE0000, 0xAEFFFF, "US Military"),
    (0xACC000, 0xACFFFF, "US Military reserve"),
]

# Known specific military hex codes (add as you discover them)
MIL_HEX_EXACT = {
    "ae1234": "USAF Special",
    # add more as observed
}

def check_military(ac):
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
        if isinstance(alt, int) and alt > 20000 and gs > 400:
            reasons.append("no callsign, high alt+speed (possible military/state)")

    return reasons

# --- Main ---

while True:
    try:
        url = "https://opendata.adsb.fi/api/v3/lat/-6.2/lon/106.8/dist/250"
        res = requests.get(url)
        data = res.json()

        hits = []
        for ac in data.get("ac", []):
            reasons = check_military(ac)
            if reasons:
                hits.append((ac, reasons))

        print(f"🔍 Scanned {len(data['ac'])} aircraft — {len(hits)} flagged\n")

        for ac, reasons in hits:
            callsign = str(ac.get("flight", "")).strip() or "(no callsign)"
            alt = ac.get("alt_baro") or "?"
            gs  = ac.get("gs") or "?"
            print(f"🚨 {callsign:<12} hex={ac.get('hex'):<8} "
                f"alt={str(alt):<6} gs={str(gs):<5} "
                f"→ {', '.join(reasons)}")
            
    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(5)
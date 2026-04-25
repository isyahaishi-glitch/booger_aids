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


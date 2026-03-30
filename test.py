import requests
import json
from datetime import datetime

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



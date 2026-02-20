"""
Run this script once to verify all city coordinates against the Aladhan API.
Usage: python -m scripts.verify_coordinates
"""

import requests
from app.constants import CITY_COORDINATES


def verify():
    print(f"{'Kota':<25} {'Koordinat':<30} {'Status':<10} {'Subuh'}")
    print("-" * 80)

    failed = []

    for city, (lat, lng) in sorted(CITY_COORDINATES.items()):
        url = "https://api.aladhan.com/v1/timings/20-02-2026"
        params = {
            "latitude": lat,
            "longitude": lng,
            "method": 20,
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            subuh = resp.json()["data"]["timings"]["Fajr"]
            print(f"{city:<25} ({lat:>9.4f}, {lng:>10.4f})   {'✅ OK':<10} {subuh}")
        except Exception as e:
            print(f"{city:<25} ({lat:>9.4f}, {lng:>10.4f})   {'❌ FAIL':<10} {e}")
            failed.append(city)

    print("\n" + "=" * 80)
    if failed:
        print(f"❌ {len(failed)} kota gagal: {', '.join(failed)}")
    else:
        print(f"✅ Semua {len(CITY_COORDINATES)} kota berhasil diverifikasi!")


if __name__ == "__main__":
    verify()

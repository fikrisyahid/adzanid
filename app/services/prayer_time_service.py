"""Service for fetching prayer times from the Aladhan API."""

import datetime
import requests

from app.constants import PRAYER_NAME_MAP


class PrayerTimeService:
    """Handles all communication with the Aladhan prayer times API."""

    API_BASE_URL = "https://api.aladhan.com/v1/timingsByCity"
    COUNTRY = "Indonesia"
    METHOD = 20
    TUNE = "0,1,0,2,3,2,0,1,0"

    def fetch(self, city: str) -> dict[str, str]:
        """Fetch today's prayer times for the given city.

        Returns:
            A dict mapping prayer names (e.g. "Subuh") to time strings (e.g. "04:35").

        Raises:
            requests.RequestException: On network errors.
            KeyError: On unexpected API response structure.
        """
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        url = f"{self.API_BASE_URL}/{today}"
        params = {
            "city": city,
            "country": self.COUNTRY,
            "method": self.METHOD,
            "tune": self.TUNE,
        }

        resp = requests.get(url, params=params)
        resp.raise_for_status()
        timings = resp.json()["data"]["timings"]

        prayer_times = {}
        for ui_name, api_key in PRAYER_NAME_MAP.items():
            raw_time = timings[api_key]
            prayer_times[ui_name] = raw_time.split(" ")[0]

        return prayer_times

    @staticmethod
    def today_formatted() -> str:
        """Return today's date as dd-MM-YYYY."""
        return datetime.datetime.now().strftime("%d-%m-%Y")

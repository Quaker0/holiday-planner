import requests
from datetime import date
from typing import Any, Dict, Optional


def fetch_weather(
    latitude: str, longitude: str, date: date
) -> Optional[Dict[str, Any]]:
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
            ],
            "timezone": "UTC",
            "start_date": date.isoformat(),
            "end_date": date.isoformat(),
        }
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast", params=params, timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        daily = data.get("daily") or {}

        def first_value(key: str):
            values = daily.get(key) or []
            return values[0] if values else None

        return {
            "date": first_value("time"),
            "temp_max": first_value("temperature_2m_max"),
            "temp_min": first_value("temperature_2m_min"),
            "precipitation_sum": first_value("precipitation_sum"),
        }
    except Exception:
        return None

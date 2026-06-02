"""
Open-Meteo historical weather data fetcher.
Replaces the previous Meteostat-based implementation.
No API key required — Open-Meteo is free and open.
"""

import requests
from datetime import datetime
from typing import List, NamedTuple

from .utils import calculate_degree_days, validate_coordinates, celsius_to_fahrenheit
from .exceptions import NWSAPIError

OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"


class DegreeDaysResult(NamedTuple):
    date: str
    high_temp: float
    low_temp: float
    mean_temp: float
    hdd: float
    cdd: float


def fetch_meteostat_data(
    lat: float,
    lon: float,
    start_date: str,
    end_date: str,
    base_temp: float = 65.0,
) -> List[DegreeDaysResult]:
    """
    Fetch historical daily temps from Open-Meteo, convert to °F,
    then calculate HDD/CDD with the given °F base temperature.

    Args:
        lat: Latitude
        lon: Longitude
        start_date: Start date string in YYYY-MM-DD format
        end_date: End date string in YYYY-MM-DD format
        base_temp: Base temperature in °F (default 65°F)

    Returns:
        List of DegreeDaysResult with temperatures in °F

    Raises:
        NWSAPIError: If the Open-Meteo API request fails or returns bad data
    """
    lat, lon = validate_coordinates(lat, lon)

    # Validate date strings
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        raise NWSAPIError(f"Invalid date format — expected YYYY-MM-DD: {e}")

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "temperature_unit": "celsius",
        "timezone": "UTC",
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise NWSAPIError(f"Failed to fetch Open-Meteo data: {e}")

    try:
        daily = data["daily"]
        dates = daily["time"]
        t_maxes = daily["temperature_2m_max"]
        t_mins = daily["temperature_2m_min"]
    except KeyError as e:
        raise NWSAPIError(f"Unexpected Open-Meteo response structure — missing key: {e}")

    results = []
    for date_str, t_max_c, t_min_c in zip(dates, t_maxes, t_mins):
        # Skip days with missing data
        if t_max_c is None or t_min_c is None:
            continue

        t_max_f = celsius_to_fahrenheit(t_max_c)
        t_min_f = celsius_to_fahrenheit(t_min_c)
        mean_f = (t_max_f + t_min_f) / 2.0

        hdd, cdd = calculate_degree_days(t_max_f, t_min_f, base_temp)

        results.append(
            DegreeDaysResult(
                date=date_str,
                high_temp=t_max_f,
                low_temp=t_min_f,
                mean_temp=mean_f,
                hdd=hdd,
                cdd=cdd,
            )
        )

    return results

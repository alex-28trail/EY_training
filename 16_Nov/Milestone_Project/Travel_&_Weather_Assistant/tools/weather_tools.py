
import requests
from datetime import date, datetime, timedelta


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Common city-name alternatives
CITY_ALIASES = {
    "bangalore": "Bengaluru",
    "bombay": "Mumbai",
    "calcutta": "Kolkata",
    "madras": "Chennai"
}


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


def get_coordinates(city: str, country: str = None):
    """Find a city's geographical coordinates."""

    city = city.strip()

    if not city:
        return None

    # Convert common alternative names
    search_city = CITY_ALIASES.get(city.casefold(), city)

    params = {
        "name": search_city,
        "count": 10,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(
            GEOCODING_URL,
            params=params,
            timeout=15
        )
        response.raise_for_status()

        results = response.json().get("results", [])

        if not results:
            return None

        # Filter by country if supplied
        if country:
            results = [
                result for result in results
                if result.get("country", "").casefold() == country.strip().casefold()
            ]

            if not results:
                return None

        # Prefer an exact city-name match
        exact_matches = [
            result for result in results
            if result.get("name", "").casefold() == search_city.casefold()
        ]

        if exact_matches:
            results = exact_matches

        # Prefer a city or administrative capital
        results.sort(
            key=lambda result: (
                result.get("feature_code") not in ("PPL", "PPLA", "PPLC"),
                -(result.get("population") or 0)
            )
        )

        return results[0]

    except requests.RequestException as error:
        print(f"Geocoding API error: {error}")
        return None


def get_weather(city: str, country: str = None, forecast_date: str = None):
    """Get current weather or a daily forecast for a city."""

    location = get_coordinates(city, country)

    if not location:
        return {
            "error": f"Could not find '{city}'. Please check the city and country."
        }

    latitude = location["latitude"]
    longitude = location["longitude"]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "auto"
    }

    if forecast_date:
        try:
            selected_date = date.fromisoformat(str(forecast_date))
        except ValueError:
            return {"error": "Invalid date. Use YYYY-MM-DD format."}

        today = date.today()
        last_forecast_date = today + timedelta(days=15)

        if selected_date < today or selected_date > last_forecast_date:
            return {
                "error": "Please select a date within the next 16 days."
            }

        params.update({
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max,"
                "sunrise,"
                "sunset"
            ),
            "start_date": selected_date.isoformat(),
            "end_date": selected_date.isoformat()
        })

    else:
        params["current"] = (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "is_day,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        )

    try:
        response = requests.get(
            WEATHER_URL,
            params=params,
            timeout=15
        )
        response.raise_for_status()

        data = response.json()

        result = {
            "city": location["name"],
            "country": location.get("country"),
            "latitude": latitude,
            "longitude": longitude
        }

        if forecast_date:
            daily = data.get("daily", {})

            if not daily.get("time"):
                return {"error": "Forecast data is unavailable for this date."}

            result.update({
                "forecast_date": daily["time"][0],
                "weather": WEATHER_CODES.get(
                    daily["weather_code"][0],
                    "Unknown"
                ),
                "temperature_max": daily["temperature_2m_max"][0],
                "temperature_min": daily["temperature_2m_min"][0],
                "precipitation_probability": (
                    daily["precipitation_probability_max"][0]
                ),
                "sunrise": daily["sunrise"][0],
                "sunset": daily["sunset"][0]
            })

        else:
            current = data.get("current", {})

            if not current:
                return {"error": "Current weather data is unavailable."}

            result.update({
                "temperature": current.get("temperature_2m"),
                "feels_like": current.get("apparent_temperature"),
                "humidity": current.get("relative_humidity_2m"),
                "precipitation": current.get("precipitation"),
                "wind_speed": current.get("wind_speed_10m"),
                "weather": WEATHER_CODES.get(
                    current.get("weather_code"),
                    "Unknown"
                ),
                "is_day": bool(current.get("is_day"))
            })

        return result

    except requests.RequestException as error:
        return {
            "error": f"Weather API request failed: {error}"
        }

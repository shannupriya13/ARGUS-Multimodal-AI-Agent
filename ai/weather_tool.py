import requests


def get_weather(city: str) -> str:
    # Convert city name to coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=10
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return f"Could not find the city: {city}"

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]
    country = location.get("country", "")

    # Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        },
        timeout=10
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()
    current = weather_data["current"]

    return (
        f"Weather in {city_name}, {country}\n"
        f"Temperature: {current['temperature_2m']}°C\n"
        f"Humidity: {current['relative_humidity_2m']}%\n"
        f"Wind speed: {current['wind_speed_10m']} km/h\n"
        f"Weather code: {current['weather_code']}"
    )
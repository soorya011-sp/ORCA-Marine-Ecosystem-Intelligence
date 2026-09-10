import requests


def get_weather_data(lat, lon):
    """
    Get current weather and marine conditions
    using Open-Meteo APIs.
    """

    weather_url = "https://api.open-meteo.com/v1/forecast"

    marine_url = "https://marine-api.open-meteo.com/v1/marine"

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "wind_speed_10m",
            "precipitation",
            "weather_code"
        ],
        "forecast_days": 1
    }

    marine_params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "wave_height",
            "wind_wave_height"
        ],
        "forecast_days": 1
    }

    result = {
        "source": "Open-Meteo",
        "latitude": lat,
        "longitude": lon
    }

    # --------------------------------------------------
    # Weather data
    # --------------------------------------------------

    try:
        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=15
        )

        response.raise_for_status()

        weather = response.json()

        current_weather = weather.get(
            "current",
            {}
        )

        result["wind_speed"] = current_weather.get(
            "wind_speed_10m"
        )

        result["rainfall"] = current_weather.get(
            "precipitation"
        )

        result["weather_code"] = current_weather.get(
            "weather_code"
        )

    except Exception as e:

        result["weather_error"] = str(e)

    # --------------------------------------------------
    # Marine data
    # --------------------------------------------------

    try:
        response = requests.get(
            marine_url,
            params=marine_params,
            timeout=15
        )

        response.raise_for_status()

        marine = response.json()

        current_marine = marine.get(
            "current",
            {}
        )

        result["wave_height"] = current_marine.get(
            "wave_height"
        )

        result["wind_wave_height"] = current_marine.get(
            "wind_wave_height"
        )

    except Exception as e:

        result["marine_error"] = str(e)

    return result


# ------------------------------------------------------
# Test
# ------------------------------------------------------

if __name__ == "__main__":

    result = get_weather_data(
        9.5,
        76.0
    )

    print(result)
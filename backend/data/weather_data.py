
import requests


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"


def weather_code_to_condition(weather_code):
    if weather_code is None:
        return "Unknown"

    try:
        weather_code = int(weather_code)
    except Exception:
        return "Unknown"

    if weather_code == 0:
        return "Clear Sky"
    if weather_code in [1, 2, 3]:
        return "Partly Cloudy"
    if weather_code in [45, 48]:
        return "Fog"
    if weather_code in [51, 53, 55]:
        return "Drizzle"
    if weather_code in [56, 57]:
        return "Freezing Drizzle"
    if weather_code in [61, 63, 65]:
        return "Rain"
    if weather_code in [66, 67]:
        return "Freezing Rain"
    if weather_code in [71, 73, 75, 77]:
        return "Snow"
    if weather_code in [80, 81, 82]:
        return "Rain Showers"
    if weather_code in [85, 86]:
        return "Snow Showers"
    if weather_code == 95:
        return "Thunderstorm"
    if weather_code in [96, 99]:
        return "Thunderstorm with Hail"

    return "Unknown"


def get_weather_data(lat, lon):

    result = {
        "source": "Open-Meteo",
        "latitude": lat,
        "longitude": lon,
        "wind_speed": None,
        "wind_direction": None,
        "wave_height": None,
        "wind_wave_height": None,
        "rainfall": None,
        "weather_code": None,
        "weather_condition": "Unknown"
    }

    # ==============================
    # WEATHER
    # ==============================

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "wind_speed_10m,wind_direction_10m,precipitation,weather_code"
    }

    weather_success = False

    # Primary: Open-Meteo
    try:
        response = requests.get(
            WEATHER_URL,
            params=weather_params,
            timeout=8,
            headers={
                "User-Agent": "ORCA-Marine-Ecosystem-Intelligence/1.0"
            }
        )

        response.raise_for_status()

        weather = response.json()
        current = weather.get("current", {})

        wind_speed = current.get("wind_speed_10m")
        wind_direction = current.get("wind_direction_10m")
        rainfall = current.get("precipitation")
        weather_code = current.get("weather_code")

        if (
            wind_speed is not None
            and wind_direction is not None
            and rainfall is not None
            and weather_code is not None
        ):
            result["wind_speed"] = wind_speed
            result["wind_direction"] = wind_direction
            result["rainfall"] = rainfall
            result["weather_code"] = weather_code
            result["weather_condition"] = weather_code_to_condition(
                weather_code
            )

            weather_success = True

            print("OPEN-METEO WEATHER SUCCESS:", weather)

        else:
            print("OPEN-METEO WEATHER INCOMPLETE:", weather)

    except Exception as e:
        print("OPEN-METEO WEATHER FAILED:", str(e))

    # ==============================
    # FALLBACK: wttr.in
    # ==============================

    if not weather_success:
        try:
            fallback_url = f"https://wttr.in/{lat},{lon}"

            fallback_response = requests.get(
                fallback_url,
                params={"format": "j1"},
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            fallback_response.raise_for_status()

            fallback_data = fallback_response.json()

            current = fallback_data.get(
                "current_condition",
                []
            )

            if current:
                current = current[0]

                result["wind_speed"] = float(
                    current.get("windspeedKmph", 0)
                )

                result["wind_direction"] = float(
                    current.get("winddirDegree", 0)
                )

                result["rainfall"] = float(
                    current.get("precipMM", 0)
                )

                result["weather_code"] = int(
                    current.get("weatherCode", 0)
                )

                result["weather_condition"] = (
                    current.get("weatherDesc", [{}])[0]
                    .get("value", "Unknown")
                )

                result["source"] = "wttr.in"

                print(
                    "WTTR.IN WEATHER SUCCESS:",
                    current
                )

            else:
                result["weather_error"] = (
                    "wttr.in returned no current_condition data"
                )

        except Exception as e:
            result["weather_error"] = (
                f"Fallback: {type(e).__name__}: {str(e)}"
            )

            print(
                "WTTR.IN WEATHER FAILED:",
                result["weather_error"]
            )

    # ==============================
    # MARINE
    # ==============================

    marine_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "wave_height,wind_wave_height"
    }

    try:
        response = requests.get(
            MARINE_URL,
            params=marine_params,
            timeout=20,
            headers={
                "User-Agent": "ORCA-Marine-Ecosystem-Intelligence/1.0"
            }
        )

        response.raise_for_status()

        marine = response.json()

        print("OPEN-METEO MARINE RESPONSE:", marine)

        current_marine = marine.get("current", {})

        result["wave_height"] = current_marine.get(
            "wave_height"
        )

        result["wind_wave_height"] = current_marine.get(
            "wind_wave_height"
        )

    except Exception as e:

        result["marine_error"] = (
            f"{type(e).__name__}: {str(e)}"
        )

        print(
            "OPEN-METEO MARINE ERROR:",
            result["marine_error"]
        )

    return result


if __name__ == "__main__":

    result = get_weather_data(9.5, 76.0)

    print("\nORCA WEATHER TEST")
    print("=================")

    print(
        "Wind Speed:",
        result.get("wind_speed"),
        "km/h"
    )

    print(
        "Wind Direction:",
        result.get("wind_direction"),
        "degrees"
    )

    print(
        "Wave Height:",
        result.get("wave_height"),
        "m"
    )

    print(
        "Wind Wave Height:",
        result.get("wind_wave_height"),
        "m"
    )

    print(
        "Rainfall:",
        result.get("rainfall"),
        "mm"
    )

    print(
        "Weather Code:",
        result.get("weather_code")
    )

    print(
        "Weather Condition:",
        result.get("weather_condition")
    )

    if result.get("weather_error"):
        print(
            "Weather Error:",
            result.get("weather_error")
        )

    if result.get("marine_error"):
        print(
            "Marine Error:",
            result.get("marine_error")
        )

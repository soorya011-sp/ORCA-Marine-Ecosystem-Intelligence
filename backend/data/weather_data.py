import requests


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"


def weather_code_to_condition(weather_code):
    try:
        code = int(weather_code)
    except (TypeError, ValueError):
        return "Clear"

    conditions = {
        0: "Clear",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Drizzle",
        53: "Drizzle",
        55: "Drizzle",
        56: "Freezing Drizzle",
        57: "Freezing Drizzle",
        61: "Rain",
        63: "Rain",
        65: "Heavy Rain",
        66: "Freezing Rain",
        67: "Freezing Rain",
        71: "Snow",
        73: "Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Rain Showers",
        81: "Rain Showers",
        82: "Heavy Rain Showers",
        85: "Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm",
        99: "Thunderstorm"
    }

    return conditions.get(code, "Clear")


def get_weather_data(lat, lon):

    result = {
        "source": "Open-Meteo",
        "latitude": lat,
        "longitude": lon,
        "wind_speed": None,
        "wind_direction": None,
        "wave_height": None,
        "wind_wave_height": None,
        "rainfall": 0,
        "weather_code": None,
        "weather_condition": "Clear"
    }

    # ============================================================
    # WEATHER - OPEN METEO
    # ============================================================

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "wind_speed_10m,"
            "wind_direction_10m,"
            "precipitation,"
            "weather_code"
        )
    }

    weather_success = False

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

        result["wind_speed"] = current.get("wind_speed_10m")
        result["wind_direction"] = current.get("wind_direction_10m")
        result["rainfall"] = current.get("precipitation") or 0
        result["weather_code"] = current.get("weather_code")

        # Convert weather code into readable condition
        if result["weather_code"] is not None:
            result["weather_condition"] = weather_code_to_condition(
                result["weather_code"]
            )

        weather_success = True

        print(
            "OPEN-METEO WEATHER SUCCESS:",
            {
                "wind_speed": result["wind_speed"],
                "wind_direction": result["wind_direction"],
                "rainfall": result["rainfall"],
                "weather_code": result["weather_code"],
                "weather_condition": result["weather_condition"]
            }
        )

    except Exception as e:

        print(
            "OPEN-METEO WEATHER FAILED:",
            str(e)
        )

    # ============================================================
    # FALLBACK - WTTR.IN
    # ============================================================

    if not weather_success:

        try:

            fallback_url = f"https://wttr.in/{lat},{lon}"

            fallback_response = requests.get(
                fallback_url,
                params={
                    "format": "j1"
                },
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            fallback_response.raise_for_status()

            fallback_data = fallback_response.json()

            current_conditions = fallback_data.get(
                "current_condition",
                []
            )

            if current_conditions:

                current = current_conditions[0]

                result["wind_speed"] = float(
                    current.get(
                        "windspeedKmph",
                        0
                    ) or 0
                )

                result["wind_direction"] = float(
                    current.get(
                        "winddirDegree",
                        0
                    ) or 0
                )

                result["rainfall"] = float(
                    current.get(
                        "precipMM",
                        0
                    ) or 0
                )

                weather_code_value = current.get(
                    "weatherCode",
                    0
                )

                try:
                    result["weather_code"] = int(
                        weather_code_value
                    )
                except Exception:
                    result["weather_code"] = 0

                weather_desc = (
                    current.get(
                        "weatherDesc",
                        [{}]
                    )[0]
                    .get(
                        "value",
                        ""
                    )
                    .strip()
                )

                if weather_desc:
                    result["weather_condition"] = weather_desc
                else:
                    result["weather_condition"] = (
                        weather_code_to_condition(
                            result["weather_code"]
                        )
                    )

                # wttr.in code 353 = light rain showers
                if result["weather_code"] == 353:
                    result["weather_condition"] = (
                        "Light Rain Showers"
                    )

                result["source"] = "wttr.in"

                print(
                    "WTTR.IN WEATHER SUCCESS:",
                    {
                        "wind_speed": result["wind_speed"],
                        "wind_direction": result["wind_direction"],
                        "rainfall": result["rainfall"],
                        "weather_code": result["weather_code"],
                        "weather_condition": result["weather_condition"]
                    }
                )

            else:

                print(
                    "WTTR.IN returned no current_condition data"
                )

        except Exception as e:

            result["weather_error"] = (
                f"Fallback: {type(e).__name__}: {str(e)}"
            )

            print(
                "WTTR.IN WEATHER FAILED:",
                result["weather_error"]
            )

    # ============================================================
    # FINAL WEATHER CONDITION SAFETY
    # ============================================================

    condition = result.get("weather_condition")

    if (
        condition is None
        or str(condition).strip() == ""
        or str(condition).strip().lower() == "unknown"
    ):

        rainfall = result.get("rainfall") or 0
        wind_speed = result.get("wind_speed") or 0

        if rainfall > 0:
            result["weather_condition"] = "Rain"
        elif wind_speed >= 30:
            result["weather_condition"] = "Windy"
        else:
            result["weather_condition"] = "Clear"

    # ============================================================
    # MARINE DATA
    # ============================================================

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

        current_marine = marine.get(
            "current",
            {}
        )

        result["wave_height"] = (
            current_marine.get(
                "wave_height"
            )
        )

        result["wind_wave_height"] = (
            current_marine.get(
                "wind_wave_height"
            )
        )

        print(
            "OPEN-METEO MARINE RESPONSE:",
            {
                "wave_height": result["wave_height"],
                "wind_wave_height": result["wind_wave_height"]
            }
        )

    except Exception as e:

        result["marine_error"] = (
            f"{type(e).__name__}: {str(e)}"
        )

        print(
            "OPEN-METEO MARINE ERROR:",
            result["marine_error"]
        )

    # ============================================================
    # FINAL GUARANTEE
    # ============================================================

    if not result.get("weather_condition"):
        result["weather_condition"] = "Clear"

    if result["weather_condition"] == "Unknown":
        result["weather_condition"] = "Clear"

    return result


# ================================================================
# LOCAL TEST
# ================================================================

if __name__ == "__main__":

    result = get_weather_data(
        9.5,
        76.0
    )

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
import math


def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    earth_radius = 6371.0

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1_rad)
        *
        math.cos(lat2_rad)
        *
        math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


def interpolate_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
    steps=10
):
    route_points = []

    for i in range(steps + 1):
        ratio = i / steps

        latitude = (
            start_lat
            +
            (end_lat - start_lat) * ratio
        )

        longitude = (
            start_lon
            +
            (end_lon - start_lon) * ratio
        )

        route_points.append({
            "latitude": round(latitude, 6),
            "longitude": round(longitude, 6)
        })

    return route_points


def evaluate_route_safety(
    wind_speed,
    wave_height,
    rainfall,
    weather_condition
):
    hazards = []
    score = 0

    if wind_speed >= 40:
        hazards.append("Very high wind speed")
        score += 3

    elif wind_speed >= 25:
        hazards.append("High wind speed")
        score += 2

    elif wind_speed >= 15:
        hazards.append("Elevated wind speed")
        score += 1

    if wave_height >= 3:
        hazards.append("High wave height")
        score += 3

    elif wave_height >= 2:
        hazards.append("Moderate wave height")
        score += 1

    if rainfall >= 50:
        hazards.append("Heavy rainfall")
        score += 2

    elif rainfall >= 20:
        hazards.append("Moderate rainfall")
        score += 1

    severe_conditions = [
        "Storm",
        "Cyclone",
        "Thunderstorm",
        "Thunderstorm with Hail"
    ]

    if weather_condition in severe_conditions:
        hazards.append(
            f"Severe weather: {weather_condition}"
        )
        score += 3

    if score >= 6:
        safety = "High Risk"

    elif score >= 3:
        safety = "Moderate Risk"

    elif score >= 1:
        safety = "Caution"

    else:
        safety = "Low Risk"

    return {
        "safety": safety,
        "score": score,
        "hazards": hazards
    }


def analyze_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
    wind_speed,
    wave_height,
    rainfall,
    weather_condition
):
    distance = calculate_distance(
        start_lat,
        start_lon,
        end_lat,
        end_lon
    )

    route_points = interpolate_route(
        start_lat,
        start_lon,
        end_lat,
        end_lon
    )

    safety_result = evaluate_route_safety(
        wind_speed=wind_speed,
        wave_height=wave_height,
        rainfall=rainfall,
        weather_condition=weather_condition
    )

    if safety_result["safety"] == "Low Risk":
        recommendation = "Route is environmentally favorable."

    elif safety_result["safety"] == "Caution":
        recommendation = (
            "Route may be usable, but the crew should "
            "monitor changing marine conditions."
        )

    elif safety_result["safety"] == "Moderate Risk":
        recommendation = (
            "Use caution. Consider delaying travel or "
            "checking an alternative route."
        )

    else:
        recommendation = (
            "Route has significant environmental safety "
            "concerns. Avoid travel until conditions improve."
        )

    return {
        "start": {
            "latitude": start_lat,
            "longitude": start_lon
        },

        "destination": {
            "latitude": end_lat,
            "longitude": end_lon
        },

        "distance_km": round(
            distance,
            2
        ),

        "route_points": route_points,

        "marine_conditions": {
            "wind_speed": wind_speed,
            "wave_height": wave_height,
            "rainfall": rainfall,
            "weather_condition": weather_condition
        },

        "safety": safety_result,

        "recommendation": recommendation,

        "method": (
            "ORCA evaluates the proposed route using "
            "marine weather conditions and identifies "
            "potential environmental hazards along the "
            "decision-support route."
        ),

        "scientific_note": (
            "This is a marine safety decision-support "
            "assessment. It does not guarantee safe "
            "navigation and should not replace official "
            "marine warnings or professional navigation."
        )
    }
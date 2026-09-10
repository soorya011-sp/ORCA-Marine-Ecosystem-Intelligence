def generate_alerts(
    wind_speed,
    wave_height,
    rainfall,
    weather_condition,
    route_result=None,
    geofence_result=None
):
    alerts = []

    if wind_speed is not None:

        if wind_speed >= 40:
            alerts.append({
                "level": "High",
                "type": "Wind",
                "message": (
                    "Very high wind speed detected. "
                    "Marine travel may be unsafe."
                )
            })

        elif wind_speed >= 25:
            alerts.append({
                "level": "Moderate",
                "type": "Wind",
                "message": (
                    "High wind speed detected. "
                    "Monitor marine conditions."
                )
            })

    if wave_height is not None:

        if wave_height >= 3:
            alerts.append({
                "level": "High",
                "type": "Waves",
                "message": (
                    "High wave height detected. "
                    "Small-vessel operations may be hazardous."
                )
            })

        elif wave_height >= 2:
            alerts.append({
                "level": "Moderate",
                "type": "Waves",
                "message": (
                    "Moderate wave conditions detected."
                )
            })

    if rainfall is not None:

        if rainfall >= 50:
            alerts.append({
                "level": "High",
                "type": "Rainfall",
                "message": (
                    "Heavy rainfall detected. "
                    "Visibility and navigation conditions may deteriorate."
                )
            })

        elif rainfall >= 20:
            alerts.append({
                "level": "Moderate",
                "type": "Rainfall",
                "message": (
                    "Moderate rainfall detected."
                )
            })

    severe_weather = [
        "Storm",
        "Cyclone",
        "Thunderstorm",
        "Thunderstorm with Hail"
    ]

    if weather_condition in severe_weather:
        alerts.append({
            "level": "High",
            "type": "Weather",
            "message": (
                f"Severe weather condition detected: "
                f"{weather_condition}."
            )
        })

    if route_result is not None:

        route_safety = (
            route_result
            .get("safety", {})
            .get("safety")
        )

        if route_safety == "High Risk":
            alerts.append({
                "level": "High",
                "type": "Route",
                "message": (
                    "The evaluated route has a high marine "
                    "safety risk."
                )
            })

        elif route_safety == "Moderate Risk":
            alerts.append({
                "level": "Moderate",
                "type": "Route",
                "message": (
                    "The evaluated route has moderate "
                    "marine safety risk."
                )
            })

    if geofence_result is not None:

        if (
            geofence_result.get("status")
            == "Geofence Violation"
        ):
            alerts.append({
                "level": "High",
                "type": "Geofence",
                "message": (
                    "The proposed route intersects a "
                    "restricted marine zone."
                )
            })

    if not alerts:
        alerts.append({
            "level": "Info",
            "type": "System",
            "message": (
                "No significant automated marine alerts "
                "were detected from the supplied conditions."
            )
        })

    high_count = sum(
        1
        for alert in alerts
        if alert["level"] == "High"
    )

    moderate_count = sum(
        1
        for alert in alerts
        if alert["level"] == "Moderate"
    )

    if high_count > 0:
        overall_level = "High"

    elif moderate_count > 0:
        overall_level = "Moderate"

    else:
        overall_level = "Low"

    return {
        "overall_level": overall_level,
        "alert_count": len(alerts),
        "high_alerts": high_count,
        "moderate_alerts": moderate_count,
        "alerts": alerts,
        "scientific_note": (
            "ORCA alerts are automated decision-support "
            "signals based on available environmental and "
            "geospatial information. Official marine warnings "
            "and professional judgment should take priority."
        )
    }
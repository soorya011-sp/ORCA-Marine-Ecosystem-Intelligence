def analyze_weather(
    wind_speed,
    wave_height,
    rainfall,
    weather_condition
):
    risks = []

    # Wind risk
    if wind_speed >= 40:
        risks.append("Very high wind speed")
    elif wind_speed >= 25:
        risks.append("High wind speed")

    # Wave risk
    if wave_height >= 3:
        risks.append("High wave height")
    elif wave_height >= 2:
        risks.append("Moderate wave height")

    # Rain risk
    if rainfall >= 50:
        risks.append("Heavy rainfall")
    elif rainfall >= 20:
        risks.append("Moderate rainfall")

    # Weather condition
    if weather_condition.lower() in [
        "storm",
        "cyclone",
        "thunderstorm"
    ]:
        risks.append(
            "Severe weather condition detected"
        )

    # Overall safety
    if any(
        "Very high" in risk or
        "Severe" in risk
        for risk in risks
    ):
        safety_risk = "High"

    elif len(risks) >= 2:
        safety_risk = "Moderate"

    elif len(risks) == 1:
        safety_risk = "Caution"

    else:
        safety_risk = "Low"

    return {
        "wind_speed": wind_speed,
        "wave_height": wave_height,
        "rainfall": rainfall,
        "weather_condition": weather_condition,
        "safety_risk": safety_risk,
        "risks": risks
    }


if __name__ == "__main__":

    result = analyze_weather(
        30,
        2.5,
        10,
        "Cloudy"
    )

    print(result)
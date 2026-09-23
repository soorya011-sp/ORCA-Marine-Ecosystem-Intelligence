def calculate_uncertainty(
    temperature,
    chlorophyll,
    salinity
):
    reasons = []
    uncertainty = 0

    # Missing or weak environmental information
    if temperature is None:
        uncertainty += 30
        reasons.append("Temperature data unavailable")

    if chlorophyll is None:
        uncertainty += 30
        reasons.append("Chlorophyll data unavailable")

    if salinity is None:
        uncertainty += 20
        reasons.append("Salinity data unavailable")

    # Limited number of indicators
    if temperature is not None and chlorophyll is not None:
        uncertainty += 10
        reasons.append(
            "Assessment currently uses a limited set of environmental indicators"
        )

    confidence = max(0, 100 - uncertainty)

    if confidence >= 80:
        level = "Low uncertainty"
    elif confidence >= 60:
        level = "Moderate uncertainty"
    else:
        level = "High uncertainty"

    return {
        "confidence": confidence,
        "uncertainty_level": level,
        "uncertainty_reasons": reasons
    }

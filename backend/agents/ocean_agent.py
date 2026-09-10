def analyze_ocean(temperature, chlorophyll, salinity):
    """
    Analyze marine environmental conditions using:

    - Sea Surface Temperature (SST)
    - Chlorophyll
    - Salinity

    This is an environmental stress assessment.
    It is NOT a biological population estimate.
    """

    factors = []
    positive_indicators = []

    # ========================================================
    # SEA SURFACE TEMPERATURE
    # ========================================================

    if temperature is None:
        factors.append("Sea surface temperature data unavailable")

    else:

        if temperature > 30:
            factors.append(
                "High sea surface temperature"
            )

        elif temperature > 29:
            factors.append(
                "Elevated sea surface temperature"
            )

        elif temperature < 24:
            factors.append(
                "Low sea surface temperature"
            )

        else:
            positive_indicators.append(
                "Sea surface temperature is within the ORCA assessment range"
            )

    # ========================================================
    # CHLOROPHYLL
    # ========================================================

    if chlorophyll is None:

        factors.append(
            "Chlorophyll data unavailable"
        )

    else:

        if chlorophyll < 0.2:

            factors.append(
                "Very low chlorophyll concentration"
            )

        elif chlorophyll < 0.5:

            factors.append(
                "Low chlorophyll concentration"
            )

        elif chlorophyll >= 1.0:

            positive_indicators.append(
                "High chlorophyll indicates higher primary productivity potential"
            )

        else:

            positive_indicators.append(
                "Moderate chlorophyll concentration"
            )

    # ========================================================
    # SALINITY
    # ========================================================

    if salinity is None:

        factors.append(
            "Salinity data unavailable"
        )

    else:

        if salinity < 32:

            factors.append(
                "Low salinity"
            )

        elif salinity > 37:

            factors.append(
                "High salinity"
            )

        else:

            positive_indicators.append(
                "Salinity is within the ORCA assessment range"
            )

    # ========================================================
    # STRESS SCORE
    # ========================================================

    stress_score = 0

    if temperature is not None:

        if temperature > 30:
            stress_score += 2

        elif temperature > 29:
            stress_score += 1

        elif temperature < 24:
            stress_score += 1

    if chlorophyll is not None:

        if chlorophyll < 0.2:
            stress_score += 2

        elif chlorophyll < 0.5:
            stress_score += 1

    if salinity is not None:

        if salinity < 32 or salinity > 37:
            stress_score += 1

    # ========================================================
    # CONDITION
    # ========================================================

    if stress_score >= 4:

        condition = "High Stress"

    elif stress_score >= 2:

        condition = "Moderate Stress"

    elif stress_score == 1:

        condition = "Mild Stress"

    else:

        condition = "Normal"

    # ========================================================
    # INTERPRETATION
    # ========================================================

    if condition == "High Stress":

        interpretation = (
            "Multiple environmental indicators show conditions "
            "that may be unfavorable for marine ecosystem processes. "
            "Further biological and oceanographic evidence is recommended."
        )

    elif condition == "Moderate Stress":

        interpretation = (
            "Some environmental indicators show potential stress. "
            "The observed conditions should be interpreted together "
            "with biological observations and historical variability."
        )

    elif condition == "Mild Stress":

        interpretation = (
            "A limited environmental stress signal is present. "
            "This does not by itself indicate a change in fish abundance."
        )

    else:

        interpretation = (
            "The supplied environmental indicators do not show "
            "a strong stress signal."
        )

    # ========================================================
    # RESULT
    # ========================================================

    return {

        "ocean_condition": condition,

        "stress_score": stress_score,

        "factors": factors,

        "positive_indicators": positive_indicators,

        "temperature": temperature,

        "chlorophyll": chlorophyll,

        "salinity": salinity,

        "interpretation": interpretation,

        "scientific_note": (
            "ORCA evaluates environmental conditions using "
            "available indicators. Environmental suitability "
            "does not directly prove fish abundance, biomass "
            "or catch probability."
        )
    }
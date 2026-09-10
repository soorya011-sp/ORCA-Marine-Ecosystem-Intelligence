def analyze_fish(species, temperature, chlorophyll):

    risk_factors = []

    # Handle missing temperature data
    if temperature is None:
        risk_factors.append(
            "Sea surface temperature data unavailable"
        )
    elif temperature > 29:
        risk_factors.append(
            "High sea surface temperature"
        )

    # Handle missing chlorophyll data
    if chlorophyll is None:
        risk_factors.append(
            "Chlorophyll data unavailable"
        )
    elif chlorophyll < 0.5:
        risk_factors.append(
            "Low chlorophyll concentration"
        )

    # Calculate risk
    if temperature is None and chlorophyll is None:
        risk = "Unknown"

    elif (
        temperature is not None
        and chlorophyll is not None
        and temperature > 29
        and chlorophyll < 0.5
    ):
        risk = "High"

    elif (
        (temperature is not None and temperature > 29)
        or
        (chlorophyll is not None and chlorophyll < 0.5)
    ):
        risk = "Moderate"

    else:
        risk = "Low"

    return {
        "species": species,
        "risk": risk,
        "risk_factors": risk_factors,
        "temperature": temperature,
        "chlorophyll": chlorophyll,
        "data_available": (
            temperature is not None
            or chlorophyll is not None
        ),
        "scientific_note": (
            "Fish risk represents an environmental "
            "assessment based on available indicators. "
            "It does not directly estimate fish abundance "
            "or catch probability."
        )
    }
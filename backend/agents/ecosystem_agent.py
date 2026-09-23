def analyze_ecosystem(
    fish_risk,
    ocean_condition,
    temperature,
    chlorophyll
):
    factors = []

    if fish_risk in ["Moderate", "High"]:
        factors.append(
            "Fish environmental risk indicators are elevated"
        )

    normalized_ocean = str(ocean_condition).lower()

    if normalized_ocean in [
        "moderate stress",
        "high stress"
    ]:
        factors.append(
            "Ocean conditions show environmental stress"
        )

    if temperature is None:
        factors.append(
            "Sea surface temperature data unavailable"
        )
    elif temperature > 29:
        factors.append(
            "High temperature may affect fish habitat suitability"
        )

    if chlorophyll is None:
        factors.append(
            "Chlorophyll data unavailable"
        )
    elif chlorophyll < 0.5:
        factors.append(
            "Low chlorophyll may indicate reduced food availability"
        )

    if (
        temperature is None
        and chlorophyll is None
        and not factors
    ):
        ecosystem_status = "Unknown"
    elif (
        temperature is not None
        and chlorophyll is not None
        and temperature > 29
        and chlorophyll < 0.5
    ):
        ecosystem_status = "High stress"
    elif len(factors) >= 3:
        ecosystem_status = "Moderate stress"
    elif len(factors) >= 1:
        ecosystem_status = "Mild stress"
    else:
        ecosystem_status = "Stable"

    return {
        "ecosystem_status": ecosystem_status,
        "factors": factors,
        "temperature": temperature,
        "chlorophyll": chlorophyll,
        "data_available": (
            temperature is not None
            or chlorophyll is not None
        ),
        "scientific_note": (
            "ORCA evaluates ecosystem environmental stress "
            "using available indicators. This assessment does "
            "not directly estimate fish abundance, biomass "
            "or catch probability."
        )
    }

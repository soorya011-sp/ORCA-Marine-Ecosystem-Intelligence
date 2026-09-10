from agents.pfz_agent import calculate_pfz_score


# ============================================================
# REAL SPATIAL PFZ ANALYSIS
# ============================================================

def analyze_spatial_pfz(marine_data):
    """
    Analyze a spatial marine grid and calculate
    Potential Fishing Zone scores.

    IMPORTANT:
    This identifies areas with potentially favorable
    environmental conditions.

    It does NOT guarantee fish presence or catch.
    """

    locations = marine_data.get(
        "locations",
        []
    )

    analyzed_locations = []

    # --------------------------------------------------------
    # Analyze every grid point locally
    # --------------------------------------------------------

    for location in locations:

        temperature = location.get(
            "temperature"
        )

        chlorophyll = location.get(
            "chlorophyll"
        )

        # ----------------------------------------------------
        # Missing data
        # ----------------------------------------------------

        if (
            temperature is None
            or
            chlorophyll is None
        ):

            analyzed_locations.append(
                {
                    **location,

                    "pfz_score": None,

                    "classification":
                        "Insufficient Data",

                    "reason":
                        "Required environmental observations "
                        "were unavailable."
                }
            )

            continue

        # ----------------------------------------------------
        # PFZ calculation
        # ----------------------------------------------------

        pfz = calculate_pfz_score(
            temperature,
            chlorophyll
        )

        analyzed_locations.append(
            {
                **location,

                "pfz_score":
                    pfz["pfz_score"],

                "classification":
                    pfz["classification"],

                "factors":
                    pfz["factors"],

                "interpretation":
                    pfz["interpretation"]
            }
        )

    # --------------------------------------------------------
    # Valid locations
    # --------------------------------------------------------

    valid_locations = [
        location
        for location in analyzed_locations
        if location["pfz_score"] is not None
    ]

    # --------------------------------------------------------
    # Sort best -> worst
    # --------------------------------------------------------

    valid_locations.sort(
        key=lambda location:
            location["pfz_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # Classification groups
    # --------------------------------------------------------

    high = [
        location
        for location in valid_locations
        if location["classification"]
        == "High Potential"
    ]

    moderate = [
        location
        for location in valid_locations
        if location["classification"]
        == "Moderate Potential"
    ]

    low = [
        location
        for location in valid_locations
        if location["classification"]
        == "Low Potential"
    ]

    insufficient = [
        location
        for location in analyzed_locations
        if location["classification"]
        == "Insufficient Data"
    ]

    # --------------------------------------------------------
    # Best zone
    # --------------------------------------------------------

    best_zone = (
        valid_locations[0]
        if valid_locations
        else None
    )

    # --------------------------------------------------------
    # Top zones
    # --------------------------------------------------------

    top_zones = valid_locations[:10]

    # --------------------------------------------------------
    # Average score
    # --------------------------------------------------------

    if valid_locations:

        average_score = round(
            sum(
                location["pfz_score"]
                for location in valid_locations
            )
            /
            len(valid_locations),
            2
        )

    else:

        average_score = None

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {

        "date":
            marine_data.get("date"),

        "data_sources":
            marine_data.get("source", []),

        "total_locations":
            len(analyzed_locations),

        "valid_locations":
            len(valid_locations),

        "high_potential_zones":
            len(high),

        "moderate_potential_zones":
            len(moderate),

        "low_potential_zones":
            len(low),

        "insufficient_data_zones":
            len(insufficient),

        "average_pfz_score":
            average_score,

        "best_zone":
            best_zone,

        "top_zones":
            top_zones,

        "locations":
            analyzed_locations,

        "scientific_note":
            (
                "PFZ classification represents potentially "
                "favorable environmental conditions based "
                "on available SST and chlorophyll indicators. "
                "It does not guarantee fish presence, "
                "aggregation or catch."
            ),

        "method":
            (
                "Spatial environmental observations were "
                "retrieved from NOAA CoastWatch and INCOIS "
                "and analyzed locally using ORCA's PFZ "
                "environmental suitability model."
            )
    }
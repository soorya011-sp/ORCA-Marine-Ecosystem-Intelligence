def calculate_pfz_score(
    temperature,
    chlorophyll
):
    """
    Calculate a Potential Fishing Zone (PFZ)
    environmental suitability score.

    This is an environmental suitability assessment,
    NOT a guarantee of fish presence.
    """

    score = 0
    factors = []

    # --------------------------------------------------
    # SST evaluation
    # --------------------------------------------------

    if 27 <= temperature <= 30:
        score += 50

        factors.append(
            "Sea surface temperature is within "
            "a potentially favorable range."
        )

    elif 25 <= temperature < 27:
        score += 35

        factors.append(
            "Sea surface temperature is moderately favorable."
        )

    elif 30 < temperature <= 32:
        score += 30

        factors.append(
            "Sea surface temperature is relatively high."
        )

    else:
        score += 15

        factors.append(
            "Sea surface temperature is outside "
            "the preferred assessment range."
        )

    # --------------------------------------------------
    # Chlorophyll evaluation
    # --------------------------------------------------

    if chlorophyll >= 1.0:
        score += 50

        factors.append(
            "High chlorophyll indicates potentially "
            "higher primary productivity."
        )

    elif chlorophyll >= 0.5:
        score += 35

        factors.append(
            "Moderate chlorophyll indicates "
            "moderate productivity."
        )

    elif chlorophyll >= 0.2:
        score += 20

        factors.append(
            "Low-to-moderate chlorophyll indicates "
            "limited productivity."
        )

    else:
        score += 10

        factors.append(
            "Low chlorophyll indicates potentially "
            "lower primary productivity."
        )

    # --------------------------------------------------
    # Final PFZ classification
    # --------------------------------------------------

    if score >= 80:
        classification = "High Potential"

    elif score >= 60:
        classification = "Moderate Potential"

    else:
        classification = "Low Potential"

    return {
        "pfz_score": score,
        "classification": classification,
        "factors": factors,
        "interpretation": (
            "PFZ represents environmental suitability "
            "based on available indicators. It does not "
            "guarantee fish presence or catch."
        )
    }


# ------------------------------------------------------
# Test
# ------------------------------------------------------

if __name__ == "__main__":

    result = calculate_pfz_score(
        temperature=28.5,
        chlorophyll=0.8
    )

    print(result)
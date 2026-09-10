def make_safety_decision(
    pfz_score,
    safety_risk,
    geofence_status,
    wave_height,
    wind_speed,
    ocean_condition="Normal"
):
    """
    Combine PFZ, weather, ocean and geofence information
    into one explainable fishing-operation recommendation.

    This is a decision-support assessment and should not
    replace official marine advisories.
    """

    reasons = []
    warnings = []
    score = 0

    # --------------------------------------------------
    # PFZ contribution
    # --------------------------------------------------

    if pfz_score is None:
        reasons.append(
            "PFZ information is unavailable."
        )

    elif pfz_score >= 80:
        score += 20
        reasons.append(
            "Environmental conditions indicate "
            "high fishing potential."
        )

    elif pfz_score >= 60:
        score += 10
        reasons.append(
            "Environmental conditions indicate "
            "moderate fishing potential."
        )

    else:
        score += 0
        reasons.append(
            "Environmental conditions indicate "
            "low fishing potential."
        )

    # --------------------------------------------------
    # Weather safety
    # --------------------------------------------------

    if safety_risk == "High":

        score -= 50

        warnings.append(
            "High weather-related safety risk."
        )

    elif safety_risk == "Moderate":

        score -= 25

        warnings.append(
            "Moderate weather-related safety risk."
        )

    elif safety_risk == "Caution":

        score -= 10

        warnings.append(
            "Weather conditions require caution."
        )

    else:

        score += 10

        reasons.append(
            "Current weather indicators are relatively favorable."
        )

    # --------------------------------------------------
    # Wave conditions
    # --------------------------------------------------

    if wave_height >= 3:

        score -= 40

        warnings.append(
            "High wave height detected."
        )

    elif wave_height >= 2:

        score -= 15

        warnings.append(
            "Moderate wave conditions detected."
        )

    # --------------------------------------------------
    # Wind conditions
    # --------------------------------------------------

    if wind_speed >= 40:

        score -= 40

        warnings.append(
            "Very high wind speed detected."
        )

    elif wind_speed >= 25:

        score -= 20

        warnings.append(
            "High wind speed detected."
        )

    # --------------------------------------------------
    # Ocean condition
    # --------------------------------------------------

    if ocean_condition == "High stress":

        score -= 15

        warnings.append(
            "Ocean indicators show high environmental stress."
        )

    elif ocean_condition == "Moderate stress":

        score -= 5

        warnings.append(
            "Ocean indicators show moderate environmental stress."
        )

    # --------------------------------------------------
    # Geofence
    # --------------------------------------------------

    if geofence_status == "Warning":

        score -= 100

        warnings.append(
            "The selected location intersects a "
            "configured restricted, protected or hazard zone."
        )

    # --------------------------------------------------
    # Final decision
    # --------------------------------------------------

    if geofence_status == "Warning":

        recommendation = "AVOID"

    elif score < 0:

        recommendation = "AVOID"

    elif score < 25:

        recommendation = "CAUTION"

    else:

        recommendation = "RECOMMENDED"

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    if recommendation == "RECOMMENDED":

        explanation = (
            "The selected location has favorable environmental "
            "conditions and no critical safety restriction was detected."
        )

    elif recommendation == "CAUTION":

        explanation = (
            "Some favorable conditions exist, but weather, ocean "
            "or environmental factors require caution."
        )

    else:

        explanation = (
            "The combined conditions indicate that fishing at "
            "this location should be avoided under the current assessment."
        )

    return {
        "recommendation": recommendation,
        "decision_score": score,
        "reasons": reasons,
        "warnings": warnings,
        "explanation": explanation,
        "scientific_note": (
            "This is a decision-support assessment based on "
            "available environmental indicators. It does not "
            "replace official marine safety advisories."
        )
    }
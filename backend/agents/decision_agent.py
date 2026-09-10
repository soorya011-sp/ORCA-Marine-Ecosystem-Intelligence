def generate_decision(
    query,
    risk_analysis=None,
    uncertainty_analysis=None,
    evidence=None,
    debate=None,
    alerts=None,
    route_analysis=None,
    geofence_analysis=None
):
    risk_analysis = risk_analysis or {}
    uncertainty_analysis = uncertainty_analysis or {}
    evidence = evidence or {}
    debate = debate or {}
    alerts = alerts or {}

    overall_risk = risk_analysis.get(
        "overall_risk",
        "Unknown"
    )

    uncertainty = uncertainty_analysis.get(
        "uncertainty_level",
        "Unknown"
    )

    evidence_items = evidence.get(
        "evidence",
        []
    )

    disagreement = debate.get(
        "disagreement_detected",
        False
    )

    alert_level = alerts.get(
        "overall_level",
        "Low"
    )

    decisions = []
    warnings = []

    if overall_risk == "High":
        decisions.append(
            "High environmental stress detected."
        )

        warnings.append(
            "Do not treat the assessment as proof "
            "of fish population decline."
        )

    elif overall_risk == "Moderate":
        decisions.append(
            "Moderate environmental stress detected."
        )

        decisions.append(
            "Continue monitoring environmental "
            "and biological conditions."
        )

    elif overall_risk == "Low":
        decisions.append(
            "No strong environmental stress signal "
            "was detected from the available indicators."
        )

    if uncertainty == "High uncertainty":
        warnings.append(
            "The assessment has high uncertainty. "
            "Additional observations are recommended."
        )

    elif uncertainty == "Moderate uncertainty":
        warnings.append(
            "Some uncertainty remains because the "
            "assessment uses a limited set of indicators."
        )

    if disagreement:
        warnings.append(
            "Specialist agents disagree. ORCA has "
            "flagged the disagreement for review."
        )

    if not evidence_items:
        warnings.append(
            "No supporting research evidence was "
            "available for this assessment."
        )

    if alert_level == "High":
        warnings.append(
            "High-priority marine alerts are present. "
            "Check official marine warnings."
        )

    if route_analysis:

        route_safety = (
            route_analysis
            .get("safety", {})
            .get("safety")
        )

        if route_safety == "High Risk":
            decisions.append(
                "The evaluated route should be avoided "
                "under the current assessed conditions."
            )

        elif route_safety == "Moderate Risk":
            decisions.append(
                "Consider delaying travel or evaluating "
                "an alternative route."
            )

    if geofence_analysis:

        if (
            geofence_analysis.get("status")
            == "Geofence Violation"
        ):
            decisions.append(
                "The proposed route intersects a "
                "restricted geofence."
            )

            warnings.append(
                "Use an alternative route and verify "
                "official maritime restrictions."
            )

    if not decisions:
        decisions.append(
            "ORCA does not have sufficient evidence "
            "to make a strong decision."
        )

    return {
        "query": query,
        "decision": decisions,
        "warnings": warnings,
        "overall_risk": overall_risk,
        "uncertainty": uncertainty,
        "evidence_count": len(evidence_items),
        "agent_disagreement": disagreement,
        "alert_level": alert_level,
        "decision_ready": True,
        "scientific_note": (
            "ORCA decisions are evidence-grounded "
            "decision-support outputs. They should not "
            "replace official marine advisories, scientific "
            "assessment or professional judgment."
        )
    }
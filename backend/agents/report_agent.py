from datetime import datetime


def generate_report(
    query,
    species=None,
    observations=None,
    fish_analysis=None,
    ocean_analysis=None,
    ecosystem_analysis=None,
    risk_analysis=None,
    uncertainty_analysis=None,
    evidence=None,
    debate=None,
    weather_analysis=None,
    route_analysis=None,
    geofence_analysis=None,
    alerts=None
):
    observations = observations or {}

    report = {
        "report_id": (
            "ORCA-"
            + datetime.utcnow().strftime(
                "%Y%m%d%H%M%S"
            )
        ),

        "generated_at": datetime.utcnow().isoformat(),

        "query": query,

        "species": species,

        "observations": observations,

        "analyses": {
            "fish": fish_analysis,
            "ocean": ocean_analysis,
            "ecosystem": ecosystem_analysis,
            "risk": risk_analysis,
            "uncertainty": uncertainty_analysis,
            "weather": weather_analysis,
            "route": route_analysis,
            "geofence": geofence_analysis
        },

        "evidence": evidence,

        "agent_debate": debate,

        "alerts": alerts
    }

    recommendations = []

    if risk_analysis:

        overall_risk = risk_analysis.get(
            "overall_risk"
        )

        if overall_risk == "High":
            recommendations.append(
                "Further investigation is recommended "
                "before making marine management decisions."
            )

        elif overall_risk == "Moderate":
            recommendations.append(
                "Monitor environmental conditions and "
                "combine them with biological observations."
            )

        elif overall_risk == "Low":
            recommendations.append(
                "No strong environmental stress signal "
                "was detected from the available indicators."
            )

    if uncertainty_analysis:

        uncertainty_level = (
            uncertainty_analysis.get(
                "uncertainty_level"
            )
        )

        if uncertainty_level == "High uncertainty":
            recommendations.append(
                "Additional observations and independent "
                "evidence are recommended because uncertainty "
                "is high."
            )

        elif uncertainty_level == "Moderate uncertainty":
            recommendations.append(
                "Interpret the assessment together with "
                "additional biological and oceanographic data."
            )

    if route_analysis:

        route_safety = (
            route_analysis
            .get("safety", {})
            .get("safety")
        )

        if route_safety == "High Risk":
            recommendations.append(
                "Avoid the evaluated route until marine "
                "conditions improve or an alternative route "
                "is assessed."
            )

        elif route_safety == "Moderate Risk":
            recommendations.append(
                "Use caution and evaluate alternative routes "
                "before travelling."
            )

    if geofence_analysis:

        if (
            geofence_analysis.get("status")
            == "Geofence Violation"
        ):
            recommendations.append(
                "Do not use the evaluated route through "
                "the detected restricted zone."
            )

    if alerts:

        if alerts.get("overall_level") == "High":
            recommendations.append(
                "High-priority marine alerts are present. "
                "Check official warnings before taking action."
            )

    if not recommendations:
        recommendations.append(
            "Continue monitoring environmental conditions "
            "and update the assessment as new observations "
            "become available."
        )

    report["recommendations"] = recommendations

    report["explainability"] = {
        "evidence_available": bool(evidence),
        "uncertainty_available": bool(
            uncertainty_analysis
        ),
        "agent_debate_available": bool(
            debate
        ),
        "multi_source_analysis": True
    }

    report["scientific_note"] = (
        "ORCA reports combine observations, specialist "
        "agent assessments, evidence and uncertainty. "
        "The report is intended for marine decision support "
        "and does not replace official advisories, scientific "
        "assessment or professional judgment."
    )

    return report
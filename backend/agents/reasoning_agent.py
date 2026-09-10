def generate_reasoning(
    species,
    temperature,
    chlorophyll,
    salinity,
    fish_result,
    ocean_result,
    ecosystem_result,
    risk_result
):
    reasoning = []
    causal_chain = []

    if temperature is None:
        reasoning.append(
            "Sea surface temperature data is unavailable."
        )
    elif temperature > 29:
        reasoning.append(
            "Sea surface temperature is elevated and may affect "
            "fish habitat suitability."
        )
        causal_chain.append("Elevated SST")
    else:
        reasoning.append(
            "Sea surface temperature does not show a strong "
            "elevated-temperature signal."
        )

    if chlorophyll is None:
        reasoning.append(
            "Chlorophyll data is unavailable."
        )
    elif chlorophyll < 0.5:
        reasoning.append(
            "Low chlorophyll may indicate reduced primary "
            "productivity and food availability."
        )
        causal_chain.append("Reduced chlorophyll")
    else:
        reasoning.append(
            "Chlorophyll does not show a strong low-productivity signal."
        )

    if salinity is None:
        reasoning.append(
            "Salinity data is unavailable."
        )
    elif salinity < 32 or salinity > 37:
        reasoning.append(
            "Unusual salinity may contribute to environmental stress."
        )
        causal_chain.append("Salinity anomaly")

    ecosystem_status = ecosystem_result.get(
        "ecosystem_status",
        "Unknown"
    )

    if ecosystem_status not in [
        "Stable",
        "Unknown"
    ]:
        reasoning.append(
            "Multiple environmental indicators suggest "
            "potential ecosystem stress."
        )

    if "Elevated SST" in causal_chain:
        causal_chain.append(
            "Possible habitat suitability change"
        )

    if "Reduced chlorophyll" in causal_chain:
        causal_chain.append(
            "Possible food availability reduction"
        )

    if len(causal_chain) >= 2:
        causal_chain.append(
            "Potential fish ecosystem stress"
        )

    if not causal_chain:
        causal_chain.append(
            "No strong stress signal detected"
        )

    return {
        "species": species,
        "overall_risk": risk_result.get(
            "overall_risk",
            "Unknown"
        ),
        "confidence": risk_result.get(
            "confidence"
        ),
        "reasoning": reasoning,
        "causal_chain": causal_chain,
        "scientific_note": (
            "ORCA reasoning links available environmental "
            "observations to possible ecological effects. "
            "These relationships are evidence-informed "
            "hypotheses and do not establish direct causation."
        )
    }
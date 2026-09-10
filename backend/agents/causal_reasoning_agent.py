def build_causal_chain(
    temperature=None,
    chlorophyll=None,
    salinity=None,
    wind_speed=None,
    wave_height=None,
    fish_risk=None,
    ocean_condition=None
):
    causal_chain = []
    evidence_links = []
    alternative_explanations = []

    if temperature is not None and temperature > 29:
        causal_chain.append({
            "factor": "Elevated sea surface temperature",
            "effect": "Potential change in fish habitat suitability",
            "confidence": "Moderate"
        })

        evidence_links.append(
            "Elevated SST can influence the biology, "
            "distribution and recruitment of pelagic fish."
        )

        alternative_explanations.append(
            "Fish distribution can also be influenced by "
            "currents, food availability and fishing pressure."
        )

    if chlorophyll is not None and chlorophyll < 0.5:
        causal_chain.append({
            "factor": "Low chlorophyll concentration",
            "effect": "Potential reduction in primary productivity",
            "confidence": "Moderate"
        })

        evidence_links.append(
            "Chlorophyll can indicate changes in "
            "phytoplankton productivity and potential food availability."
        )

        alternative_explanations.append(
            "Low chlorophyll at one location does not prove "
            "reduced regional fish productivity."
        )

    if salinity is not None:
        if salinity < 32 or salinity > 37:
            causal_chain.append({
                "factor": "Salinity anomaly",
                "effect": "Potential change in marine habitat conditions",
                "confidence": "Low"
            })

            alternative_explanations.append(
                "Salinity effects depend on species, depth, "
                "season and surrounding ocean conditions."
            )

    if wind_speed is not None and wind_speed >= 25:
        causal_chain.append({
            "factor": "Elevated wind conditions",
            "effect": "Potential change in surface mixing and navigation conditions",
            "confidence": "Moderate"
        })

    if wave_height is not None and wave_height >= 2:
        causal_chain.append({
            "factor": "Elevated wave height",
            "effect": "Potential marine operational stress",
            "confidence": "Moderate"
        })

    if fish_risk in ["Moderate", "High"]:
        causal_chain.append({
            "factor": "Environmental stress indicators",
            "effect": "Potential fish habitat or productivity stress",
            "confidence": "Moderate"
        })

    if (
        temperature is not None
        and chlorophyll is not None
        and temperature > 29
        and chlorophyll < 0.5
    ):
        causal_chain.append({
            "factor": "Combined SST and chlorophyll signal",
            "effect": "Potential ecosystem-level environmental stress",
            "confidence": "Moderate"
        })

    if not causal_chain:
        causal_chain.append({
            "factor": "No strong environmental anomaly detected",
            "effect": "No strong causal stress pathway identified",
            "confidence": "Low"
        })

    return {
        "causal_chain": causal_chain,
        "evidence_links": evidence_links,
        "alternative_explanations": list(
            dict.fromkeys(alternative_explanations)
        ),
        "causal_reasoning": (
            "ORCA links observed environmental indicators "
            "to possible ecological effects. These relationships "
            "represent evidence-informed hypotheses rather than "
            "proof of direct causation."
        ),
        "causal_inference_warning": (
            "Correlation between environmental indicators and "
            "fish outcomes does not by itself establish causation."
        )
    }
def find_evidence(species, temperature, chlorophyll):

    evidence = []

    if temperature > 29:
        evidence.append({
            "topic": "Sea Surface Temperature",
            "finding": (
                "Changes in sea surface temperature can influence "
                "the distribution, aggregation and habitat suitability "
                "of Indian oil sardine."
            ),
            "source": (
                "Overfishing and Climate Drives Changes in Biology "
                "and Recruitment of the Indian Oil Sardine"
            )
        })

    if chlorophyll < 0.5:
        evidence.append({
            "topic": "Chlorophyll",
            "finding": (
                "Chlorophyll concentration can act as an indicator "
                "of ocean productivity and potential food availability "
                "for pelagic fish."
            ),
            "source": (
                "Satellite chlorophyll concentration as an aid to "
                "understanding the dynamics of Indian oil sardine "
                "in the southeastern Arabian Sea"
            )
        })

    if not evidence:
        evidence.append({
            "topic": "Environmental Conditions",
            "finding": (
                "The supplied environmental indicators do not show "
                "strong evidence of stress."
            ),
            "source": "ORCA Environmental Analysis"
        })

    return {
        "species": species,
        "evidence": evidence
    }
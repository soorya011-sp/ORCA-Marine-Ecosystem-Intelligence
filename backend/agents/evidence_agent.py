def find_evidence(
    species,
    temperature=None,
    chlorophyll=None,
    salinity=None
):
    evidence = []

    species_lower = str(species).lower()

    # ---------------------------------------------------------
    # 1. Indian Oil Sardine - SST research
    # ---------------------------------------------------------
    if "sardine" in species_lower:
        evidence.append({
            "topic": "Sea Surface Temperature",
            "finding": (
                "Changes in sea surface temperature can influence "
                "the distribution, aggregation, habitat suitability "
                "and recruitment of Indian oil sardine."
            ),
            "source": (
                "Overfishing and Climate Drives Changes in Biology "
                "and Recruitment of the Indian Oil Sardine"
            ),
            "evidence_type": "Research evidence",
            "relevance": "High"
        })

    # ---------------------------------------------------------
    # 2. Indian Oil Sardine - Chlorophyll research
    # ---------------------------------------------------------
    if "sardine" in species_lower:
        evidence.append({
            "topic": "Chlorophyll",
            "finding": (
                "Satellite-derived chlorophyll concentration can "
                "help understand Indian oil sardine dynamics and "
                "may indicate changes in primary productivity."
            ),
            "source": (
                "Satellite chlorophyll concentration as an aid "
                "to understanding the dynamics of Indian oil sardine "
                "in the southeastern Arabian Sea"
            ),
            "evidence_type": "Research evidence",
            "relevance": "High"
        })

    # ---------------------------------------------------------
    # 3. Indian Oil Sardine aggregation research
    # ---------------------------------------------------------
    if "sardine" in species_lower:
        evidence.append({
            "topic": "Fish Aggregation",
            "finding": (
                "Indian oil sardine aggregation events have been "
                "associated with environmental conditions including "
                "sea surface temperature, phytoplankton availability, "
                "precipitation and oceanographic processes."
            ),
            "source": (
                "Investigating Indian oil sardine aggregation events "
                "in coastal waters of the southeastern Arabian Sea"
            ),
            "evidence_type": "Research evidence",
            "relevance": "High"
        })

    # ---------------------------------------------------------
    # 4. Salinity evidence
    # ---------------------------------------------------------
    if salinity is not None:

        if salinity < 32 or salinity > 37:
            salinity_relevance = "High"
        else:
            salinity_relevance = "Contextual"

        evidence.append({
            "topic": "Salinity",
            "finding": (
                "Environmental variables including salinity can "
                "contribute to variations in marine fish biology "
                "and habitat conditions."
            ),
            "source": (
                "Overfishing and Climate Drives Changes in Biology "
                "and Recruitment of the Indian Oil Sardine"
            ),
            "evidence_type": "Research evidence",
            "relevance": salinity_relevance
        })

    # ---------------------------------------------------------
    # 5. Current observation context
    # ---------------------------------------------------------

    observations = []

    if temperature is not None:
        observations.append(
            f"Observed SST: {temperature:.2f} °C"
        )
    else:
        observations.append(
            "SST observation unavailable"
        )

    if chlorophyll is not None:
        observations.append(
            f"Observed chlorophyll: {chlorophyll:.3f}"
        )
    else:
        observations.append(
            "Chlorophyll observation unavailable"
        )

    if salinity is not None:
        observations.append(
            f"Observed salinity: {salinity:.2f} PSU"
        )

    evidence.append({
        "topic": "Current Observation Context",
        "finding": (
            "ORCA compares available environmental observations "
            "with published marine ecosystem research. "
            + "; ".join(observations)
        ),
        "source": "ORCA Environmental Observation Layer",
        "evidence_type": "Observation context",
        "relevance": "Contextual"
    })

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    return {
        "species": species,
        "evidence": evidence,
        "evidence_count": len(evidence),
        "evidence_available": len(evidence) > 0
    }

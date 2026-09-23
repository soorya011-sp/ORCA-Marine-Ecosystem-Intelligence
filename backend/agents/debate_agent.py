def analyze_agent_disagreement(
    fish_result,
    ocean_result,
    ecosystem_result,
    reasoning_result=None,
    evidence_result=None
):
    """
    ORCA Debate Agent

    Compares specialist-agent assessments, identifies disagreement,
    explains why the agents may disagree, and produces a consensus
    assessment for the downstream reasoning layer.
    """

    fish_risk = fish_result.get("risk", "Unknown")
    ocean_condition = ocean_result.get(
        "ocean_condition",
        "Unknown"
    )
    ecosystem_status = ecosystem_result.get(
        "ecosystem_status",
        "Unknown"
    )

    opinions = {
        "Fish Agent": fish_risk,
        "Ocean Agent": ocean_condition,
        "Ecosystem Agent": ecosystem_status
    }

    # Convert different agent outputs to comparable
    # environmental-stress levels.
    levels = {
        "Low": 1,
        "Normal": 1,
        "Stable": 1,

        "Mild stress": 1,
        "Moderate": 2,
        "Moderate stress": 2,

        "High": 3,
        "High stress": 3,

        "Unknown": 0
    }

    scores = [
        levels.get(value, 0)
        for value in opinions.values()
    ]

    valid_scores = [
        score for score in scores
        if score > 0
    ]

    if not valid_scores:
        return {
            "agent_opinions": opinions,
            "disagreement_detected": False,
            "consensus": "Unknown",
            "consensus_score": None,
            "agreement_level": "Insufficient evidence",
            "explanation": (
                "The specialist agents could not produce "
                "enough valid assessments for a reliable "
                "comparison."
            ),
            "debate_points": [],
            "scientific_note": (
                "ORCA does not force a consensus when "
                "insufficient evidence is available."
            )
        }

    highest = max(valid_scores)
    lowest = min(valid_scores)

    disagreement = highest != lowest

    # Calculate average specialist assessment.
    average_score = sum(valid_scores) / len(valid_scores)

    if average_score >= 2.5:
        consensus = "High stress"
    elif average_score >= 1.5:
        consensus = "Moderate stress"
    else:
        consensus = "Low stress"

    # Determine agreement strength.
    score_range = highest - lowest

    if score_range == 0:
        agreement_level = "Strong agreement"
    elif score_range == 1:
        agreement_level = "Partial agreement"
    else:
        agreement_level = "Strong disagreement"

    debate_points = []

    if fish_risk in ["High", "Moderate"]:
        debate_points.append(
            "Fish Agent indicates elevated environmental risk."
        )

    if ocean_condition in [
        "High stress",
        "Moderate stress"
    ]:
        debate_points.append(
            "Ocean Agent identifies environmental stress."
        )

    if ecosystem_status in [
        "High stress",
        "Moderate stress"
    ]:
        debate_points.append(
            "Ecosystem Agent identifies broader ecosystem stress."
        )

    if fish_risk in ["Low"] and ocean_condition in [
        "High stress",
        "Moderate stress"
    ]:
        debate_points.append(
            "Fish Agent reports lower direct fish risk "
            "despite broader ocean stress."
        )

    if fish_risk in ["High", "Moderate"] and ocean_condition in [
        "Low",
        "Normal"
    ]:
        debate_points.append(
            "Fish Agent reports elevated risk while "
            "Ocean Agent reports relatively normal conditions."
        )

    if not debate_points:
        debate_points.append(
            "Specialist agents provide broadly consistent "
            "environmental assessments."
        )

    if disagreement:
        explanation = (
            "The specialist agents produced different "
            "levels of environmental stress. ORCA preserves "
            "this disagreement and evaluates the evidence "
            "before producing a final assessment."
        )
    else:
        explanation = (
            "The specialist agents produced consistent "
            "environmental assessments, increasing confidence "
            "in the combined interpretation."
        )

    # Optional reasoning context.
    reasoning_summary = None

    if reasoning_result:
        reasoning_summary = reasoning_result.get(
            "reasoning",
            []
        )

    # Optional evidence context.
    evidence_count = 0

    if evidence_result:
        if isinstance(evidence_result, dict):
            evidence_count = evidence_result.get(
                "evidence_count",
                0
            )

            # Handle nested evidence structure.
            if "evidence" in evidence_result:
                nested = evidence_result["evidence"]

                if isinstance(nested, dict):
                    evidence_count = nested.get(
                        "evidence_count",
                        evidence_count
                    )

    # Debate confidence is deliberately different from
    # statistical confidence. It represents agreement among
    # available specialist agents and evidence availability.
    debate_confidence = 0

    if len(valid_scores) >= 3:
        debate_confidence += 50

    if not disagreement:
        debate_confidence += 25
    elif score_range == 1:
        debate_confidence += 10

    if evidence_count >= 3:
        debate_confidence += 25
    elif evidence_count > 0:
        debate_confidence += 10

    debate_confidence = min(
        debate_confidence,
        100
    )

    return {
        "agent_opinions": opinions,
        "agent_scores": {
            "Fish Agent": levels.get(
                fish_risk,
                0
            ),
            "Ocean Agent": levels.get(
                ocean_condition,
                0
            ),
            "Ecosystem Agent": levels.get(
                ecosystem_status,
                0
            )
        },
        "disagreement_detected": disagreement,
        "consensus": consensus,
        "consensus_score": round(
            average_score,
            2
        ),
        "agreement_level": agreement_level,
        "debate_confidence": debate_confidence,
        "evidence_count": evidence_count,
        "debate_points": debate_points,
        "explanation": explanation,
        "reasoning_context": reasoning_summary,
        "scientific_note": (
            "ORCA treats disagreement between specialist "
            "agents as uncertainty rather than hiding it. "
            "The consensus is an evidence-informed "
            "environmental assessment and does not establish "
            "direct ecological causation."
        )
    }

def calculate_risk(fish_risk, ocean_condition, ecosystem_status):

    scores = {
        "Low": 1,
        "Normal": 1,
        "Moderate": 2,
        "Moderate stress": 2,
        "High": 3,
        "High stress": 3
    }

    fish_score = scores.get(fish_risk, 1)
    ocean_score = scores.get(ocean_condition, 1)
    ecosystem_score = scores.get(ecosystem_status, 1)

    average_score = (
        fish_score +
        ocean_score +
        ecosystem_score
    ) / 3

    if average_score >= 2.5:
        overall_risk = "High"
    elif average_score >= 1.5:
        overall_risk = "Moderate"
    else:
        overall_risk = "Low"

    confidence = round(
        (average_score / 3) * 100
    )

    return {
        "overall_risk": overall_risk,
        "confidence": confidence,
        "agent_scores": {
            "fish_agent": fish_score,
            "ocean_agent": ocean_score,
            "ecosystem_agent": ecosystem_score
        }
    }

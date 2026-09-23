def create_visualization_data(
    locations=None,
    observations=None,
    analysis=None
):
    locations = locations or []
    observations = observations or {}
    analysis = analysis or {}

    map_points = []

    for location in locations:

        latitude = location.get("latitude")
        longitude = location.get("longitude")

        if latitude is None or longitude is None:
            continue

        map_points.append({
            "latitude": latitude,
            "longitude": longitude,
            "temperature": location.get(
                "temperature"
            ),
            "chlorophyll": location.get(
                "chlorophyll"
            ),
            "pfz_score": location.get(
                "pfz_score"
            ),
            "classification": location.get(
                "classification"
            )
        })

    chart_data = []

    if observations:

        for variable, value in observations.items():

            if isinstance(
                value,
                (int, float)
            ):
                chart_data.append({
                    "variable": variable,
                    "value": value
                })

    return {
        "map": {
            "points": map_points,
            "point_count": len(map_points)
        },

        "charts": {
            "observations": chart_data
        },

        "summary": {
            "status": analysis.get(
                "overall_risk",
                analysis.get(
                    "ecosystem_status",
                    "Unknown"
                )
            ),
            "confidence": analysis.get(
                "confidence"
            )
        },

        "visualization_ready": True,

        "scientific_note": (
            "Visualizations present available marine "
            "observations and ORCA analytical outputs. "
            "They should be interpreted together with "
            "their underlying data sources and uncertainty."
        )
    }

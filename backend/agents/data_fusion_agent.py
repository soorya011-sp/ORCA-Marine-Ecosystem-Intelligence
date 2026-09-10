def normalize_value(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return value

    try:
        return float(value)
    except (ValueError, TypeError):
        return value


def fuse_marine_data(
    marine_data=None,
    weather_data=None,
    fish_analysis=None,
    ocean_analysis=None
):
    marine_data = marine_data or {}
    weather_data = weather_data or {}
    fish_analysis = fish_analysis or {}
    ocean_analysis = ocean_analysis or {}

    fused = {
        "environment": {},
        "weather": {},
        "fish": {},
        "sources": [],
        "missing_data": []
    }

    temperature = normalize_value(
        marine_data.get("temperature")
    )

    chlorophyll = normalize_value(
        marine_data.get("chlorophyll")
    )

    salinity = normalize_value(
        marine_data.get("salinity")
    )

    if temperature is not None:
        fused["environment"][
            "sea_surface_temperature"
        ] = temperature
    else:
        fused["missing_data"].append(
            "Sea surface temperature"
        )

    if chlorophyll is not None:
        fused["environment"][
            "chlorophyll"
        ] = chlorophyll
    else:
        fused["missing_data"].append(
            "Chlorophyll"
        )

    if salinity is not None:
        fused["environment"][
            "salinity"
        ] = salinity
    else:
        fused["missing_data"].append(
            "Salinity"
        )

    wind_speed = normalize_value(
        weather_data.get("wind_speed")
    )

    wave_height = normalize_value(
        weather_data.get("wave_height")
    )

    rainfall = normalize_value(
        weather_data.get("rainfall")
    )

    weather_condition = weather_data.get(
        "weather_condition"
    )

    if wind_speed is not None:
        fused["weather"][
            "wind_speed"
        ] = wind_speed
    else:
        fused["missing_data"].append(
            "Wind speed"
        )

    if wave_height is not None:
        fused["weather"][
            "wave_height"
        ] = wave_height
    else:
        fused["missing_data"].append(
            "Wave height"
        )

    if rainfall is not None:
        fused["weather"][
            "rainfall"
        ] = rainfall
    else:
        fused["missing_data"].append(
            "Rainfall"
        )

    if weather_condition is not None:
        fused["weather"][
            "weather_condition"
        ] = weather_condition

    if fish_analysis:
        fused["fish"] = {
            "risk": fish_analysis.get(
                "risk"
            ),
            "risk_factors": fish_analysis.get(
                "risk_factors",
                []
            )
        }

    if ocean_analysis:
        fused["environment"][
            "ocean_condition"
        ] = ocean_analysis.get(
            "ocean_condition"
        )

    marine_source = marine_data.get(
        "source"
    )

    if marine_source:
        if isinstance(
            marine_source,
            list
        ):
            fused["sources"].extend(
                marine_source
            )
        else:
            fused["sources"].append(
                marine_source
            )

    weather_source = weather_data.get(
        "source"
    )

    if weather_source:
        fused["sources"].append(
            weather_source
        )

    fused["sources"] = list(
        dict.fromkeys(
            fused["sources"]
        )
    )

    total_fields = (
        len(fused["environment"])
        + len(fused["weather"])
    )

    missing_count = len(
        fused["missing_data"]
    )

    if total_fields == 0:
        completeness = 0

    else:
        expected_fields = 7
        completeness = round(
            max(
                0,
                min(
                    100,
                    (
                        (
                            expected_fields
                            - missing_count
                        )
                        / expected_fields
                    )
                    * 100
                )
            )
        )

    if completeness >= 80:
        data_quality = "Good"

    elif completeness >= 50:
        data_quality = "Moderate"

    else:
        data_quality = "Limited"

    return {
        "fused_data": fused,
        "data_completeness": completeness,
        "data_quality": data_quality,
        "source_count": len(
            fused["sources"]
        ),
        "fusion_complete": True,
        "scientific_note": (
            "ORCA combines observations from multiple "
            "marine and weather sources before reasoning. "
            "Missing observations are explicitly retained "
            "instead of being silently treated as zero."
        )
    }
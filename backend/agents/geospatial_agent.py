from math import radians, sin, cos, sqrt, atan2


def calculate_distance_km(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate distance between two geographic points
    using the Haversine formula.
    """

    earth_radius = 6371.0

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        +
        cos(lat1_rad)
        * cos(lat2_rad)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return round(
        earth_radius * c,
        2
    )


def classify_zone(score):
    """
    Convert PFZ score into a map classification.
    """

    if score is None:
        return "Insufficient Data"

    if score >= 80:
        return "High Potential"

    if score >= 60:
        return "Moderate Potential"

    return "Low Potential"


def create_geojson(pfz_analysis):
    """
    Convert PFZ analysis into GeoJSON-style
    point features for map visualization.
    """

    features = []

    locations = pfz_analysis.get(
        "locations",
        []
    )

    for location in locations:

        latitude = location.get(
            "latitude"
        )

        longitude = location.get(
            "longitude"
        )

        score = location.get(
            "pfz_score"
        )

        classification = classify_zone(
            score
        )

        features.append({

            "type": "Feature",

            "geometry": {
                "type": "Point",
                "coordinates": [
                    longitude,
                    latitude
                ]
            },

            "properties": {

                "latitude": latitude,

                "longitude": longitude,

                "pfz_score": score,

                "classification": classification,

                "temperature":
                    location.get(
                        "temperature"
                    ),

                "chlorophyll":
                    location.get(
                        "chlorophyll"
                    ),

                "date":
                    location.get(
                        "date"
                    )
            }
        })

    return {

        "type": "FeatureCollection",

        "features": features
    }


def analyze_geospatial_pfz(
    pfz_analysis,
    center_lat,
    center_lon
):
    """
    Add spatial ranking and distance information
    to the PFZ results.
    """

    locations = pfz_analysis.get(
        "locations",
        []
    )

    spatial_locations = []

    for location in locations:

        latitude = location.get(
            "latitude"
        )

        longitude = location.get(
            "longitude"
        )

        score = location.get(
            "pfz_score"
        )

        distance = calculate_distance_km(
            center_lat,
            center_lon,
            latitude,
            longitude
        )

        spatial_locations.append({

            **location,

            "distance_from_center_km":
                distance,

            "classification":
                classify_zone(score)
        })

    # Best zones first
    valid = [

        x for x in spatial_locations

        if x.get("pfz_score") is not None
    ]

    valid.sort(
        key=lambda x: x["pfz_score"],
        reverse=True
    )

    geojson = create_geojson({
        "locations":
            spatial_locations
    })

    return {

        "center": {
            "latitude": center_lat,
            "longitude": center_lon
        },

        "total_locations":
            len(spatial_locations),

        "ranked_locations":
            valid,

        "best_zone":
            valid[0]
            if valid
            else None,

        "geojson":
            geojson
    }
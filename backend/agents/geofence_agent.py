import math


def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    earth_radius = 6371.0

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


def is_inside_geofence(
    latitude,
    longitude,
    center_lat,
    center_lon,
    radius_km
):
    distance = calculate_distance(
        latitude,
        longitude,
        center_lat,
        center_lon
    )

    return {
        "inside": distance <= radius_km,
        "distance_km": round(distance, 2),
        "radius_km": radius_km
    }


def analyze_geofence(
    route_points,
    restricted_zones
):
    checked_points = []
    violations = []

    for point in route_points:

        latitude = point["latitude"]
        longitude = point["longitude"]

        point_result = {
            "latitude": latitude,
            "longitude": longitude,
            "restricted": False,
            "zones": []
        }

        for zone in restricted_zones:

            result = is_inside_geofence(
                latitude,
                longitude,
                zone["center_lat"],
                zone["center_lon"],
                zone["radius_km"]
            )

            if result["inside"]:

                point_result["restricted"] = True

                point_result["zones"].append({
                    "name": zone["name"],
                    "distance_km": result["distance_km"],
                    "radius_km": zone["radius_km"],
                    "reason": zone.get(
                        "reason",
                        "Restricted marine area"
                    )
                })

                violations.append({
                    "latitude": latitude,
                    "longitude": longitude,
                    "zone": zone["name"],
                    "reason": zone.get(
                        "reason",
                        "Restricted marine area"
                    )
                })

        checked_points.append(point_result)

    if violations:
        status = "Geofence Violation"
        recommendation = (
            "The proposed route intersects one or more "
            "restricted marine zones. Consider an alternative route."
        )
    else:
        status = "Clear"
        recommendation = (
            "No restricted geofence intersection was detected "
            "for the evaluated route points."
        )

    return {
        "status": status,
        "violations": violations,
        "checked_points": checked_points,
        "recommendation": recommendation,
        "scientific_note": (
            "Geofence analysis is based on the restricted-zone "
            "boundaries supplied to ORCA. It should not be treated "
            "as a substitute for official maritime navigation charts "
            "or regulatory notices."
        )
    }
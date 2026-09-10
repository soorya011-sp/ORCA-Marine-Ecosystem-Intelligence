def route_query(query):
    query_lower = query.lower()

    routes = []

    keyword_groups = {
        "fish": [
            "fish",
            "sardine",
            "tuna",
            "mackerel",
            "catch",
            "fishing",
            "productivity",
            "fish population",
            "fish habitat"
        ],

        "ocean": [
            "ocean",
            "sea",
            "sst",
            "temperature",
            "chlorophyll",
            "salinity",
            "current",
            "productivity"
        ],

        "weather": [
            "weather",
            "wind",
            "rain",
            "rainfall",
            "wave",
            "waves",
            "storm",
            "cyclone",
            "thunderstorm"
        ],

        "pfz": [
            "pfz",
            "potential fishing zone",
            "fishing zone",
            "best fishing area",
            "where to fish"
        ],

        "route": [
            "route",
            "navigation",
            "navigate",
            "travel",
            "boat route",
            "safe route"
        ],

        "geofence": [
            "restricted zone",
            "restricted area",
            "geofence",
            "no fishing",
            "protected area",
            "hazard zone"
        ],

        "research": [
            "why",
            "reason",
            "research",
            "paper",
            "study",
            "evidence",
            "cause",
            "causes"
        ],

        "ecosystem": [
            "ecosystem",
            "marine ecosystem",
            "biodiversity",
            "environment",
            "environmental stress"
        ]
    }

    for route, keywords in keyword_groups.items():

        for keyword in keywords:

            if keyword in query_lower:
                routes.append(route)
                break

    routes = list(dict.fromkeys(routes))

    if not routes:
        routes.append("general")

    return {
        "query": query,
        "routes": routes,
        "route_count": len(routes),
        "routing_complete": True
    }


def build_execution_plan(query):
    routing = route_query(query)

    routes = routing["routes"]

    execution_order = []

    priority = [
        "weather",
        "ocean",
        "fish",
        "pfz",
        "ecosystem",
        "route",
        "geofence",
        "research"
    ]

    for route in priority:

        if route in routes:
            execution_order.append(route)

    if "general" in routes:
        execution_order = ["general"]

    execution_order.append("reasoning")

    return {
        "query": query,
        "routes": routes,
        "execution_order": execution_order,
        "parallel_processing": len(routes) > 1,
        "plan_ready": True
    }
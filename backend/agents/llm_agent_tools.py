# ============================================================
# ORCA - LLM AGENT TOOL BRIDGE
#
# Gemini can request specialist capabilities.
# ORCA executes the real functions.
#
# IMPORTANT:
# The LLM is NOT trusted with scientific state.
# Scientific values are validated and passed by ORCA.
# ============================================================

import json
from typing import Any, Dict


# ============================================================
# DATA LAYER
# ============================================================

from backend.data.marine_data import (
    get_marine_data,
    extract_marine_values,
)

from backend.data.weather_data import (
    get_weather_data,
)


# ============================================================
# SPECIALIST AGENTS
# ============================================================

from backend.agents.fish_agent import (
    analyze_fish,
)

from backend.agents.ocean_agent import (
    analyze_ocean,
)

from backend.agents.ecosystem_agent import (
    analyze_ecosystem,
)

from backend.agents.weather_agent import (
    analyze_weather,
)

from backend.agents.risk_agent import (
    calculate_risk,
)

from backend.agents.evidence_agent import (
    find_evidence,
)

from backend.agents.reasoning_agent import (
    generate_reasoning,
)

from backend.agents.uncertainty_agent import (
    calculate_uncertainty,
)

from backend.agents.debate_agent import (
    analyze_agent_disagreement,
)

from backend.agents.causal_reasoning_agent import (
    build_causal_chain,
)

from backend.agents.alert_agent import (
    generate_alerts,
)

from backend.agents.route_agent import (
    analyze_route,
)

from backend.agents.geofence_agent import (
    analyze_geofence,
)


# ============================================================
# DEFAULTS
# ============================================================
from datetime import datetime as _datetime, timedelta as _timedelta

DEFAULT_SPECIES = "Indian Oil Sardine"

DEFAULT_LAT = 9.5

DEFAULT_LON = 76.0

DEFAULT_SALINITY = 34.0

DEFAULT_DATE = (_datetime.utcnow() - _timedelta(days=1)).strftime("%Y-%m-%d")


# ============================================================
# SAFE JSON CONVERSION
# ============================================================

def safe_json_value(
    value: Any
) -> Any:

    if value is None:
        return None

    if isinstance(
        value,
        (str, int, float, bool)
    ):
        return value

    if isinstance(
        value,
        dict
    ):
        return {
            str(key): safe_json_value(item)
            for key, item in value.items()
        }

    if isinstance(
        value,
        (list, tuple)
    ):
        return [
            safe_json_value(item)
            for item in value
        ]

    try:
        return value.item()
    except Exception:
        pass

    return str(value)


# ============================================================
# WEATHER CODE
# ============================================================

def weather_code_to_condition(
    weather_code
) -> str:

    if weather_code is None:
        return "Unknown"

    if weather_code == 0:
        return "Clear"

    if weather_code in [1, 2, 3]:
        return "Partly Cloudy"

    if weather_code in [45, 48]:
        return "Fog"

    if weather_code in [51, 53, 55]:
        return "Drizzle"

    if weather_code in [61, 63, 65]:
        return "Rain"

    if weather_code in [71, 73, 75]:
        return "Snow"

    if weather_code in [80, 81, 82]:
        return "Rain Showers"

    if weather_code == 95:
        return "Thunderstorm"

    if weather_code in [96, 99]:
        return "Thunderstorm with Hail"

    return "Unknown"


# ============================================================
# MARINE OBSERVATIONS
# ============================================================

def get_marine_observations(
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    date: str = DEFAULT_DATE,
) -> Dict[str, Any]:

    try:

        marine_data = get_marine_data(
            lat,
            lon,
            date
        )

        temperature = None
        chlorophyll = None


        try:

            temperature, chlorophyll = (
                extract_marine_values(
                    marine_data
                )
            )

        except Exception:

            pass


        # ----------------------------------------------------
        # SST fallback
        # ----------------------------------------------------

        if temperature is None:

            try:

                rows = (
                    marine_data["sst"]
                    ["data"]
                    ["table"]
                    ["rows"]
                )

                if rows:

                    temperature = float(
                        rows[0][-1]
                    )

            except Exception:

                temperature = None


        # ----------------------------------------------------
        # Chlorophyll fallback
        # ----------------------------------------------------

        if chlorophyll is None:

            try:

                rows = (
                    marine_data["chlorophyll"]
                    ["data"]
                    ["table"]
                    ["rows"]
                )

                if rows:

                    chlorophyll = float(
                        rows[0][-1]
                    )

            except Exception:

                chlorophyll = None


        return {

            "success": True,

            "latitude": float(lat),

            "longitude": float(lon),

            "observation_date": str(date),

            "observations": {

                "sea_surface_temperature":
                    safe_json_value(
                        temperature
                    ),

                "chlorophyll":
                    safe_json_value(
                        chlorophyll
                    )
            },

            "units": {

                "sea_surface_temperature":
                    "°C",

                "chlorophyll":
                    "mg/m³"
            },

            "sources": {

                "sea_surface_temperature":
                    "NOAA CoastWatch MUR SST",

                "chlorophyll":
                    "INCOIS Oceansat-2 OCM"
            },

            "data_status": {

                "sea_surface_temperature":
                    temperature is not None,

                "chlorophyll":
                    chlorophyll is not None,

                "historical_observation":
                    True
            }

        }

    except Exception as exc:

        return {

            "success": False,

            "latitude": float(lat),

            "longitude": float(lon),

            "observation_date": str(date),

            "observations": {

                "sea_surface_temperature":
                    None,

                "chlorophyll":
                    None
            },

            "error":
                str(exc)
        }


# ============================================================
# MARINE WEATHER
# ============================================================

def get_marine_weather(
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
) -> Dict[str, Any]:

    try:

        weather_data = get_weather_data(
            lat,
            lon
        )


        wind_speed = weather_data.get(
            "wind_speed"
        )

        wave_height = weather_data.get(
            "wave_height"
        )

        rainfall = weather_data.get(
            "rainfall"
        )

        weather_code = weather_data.get(
            "weather_code"
        )


        weather_condition = (
            weather_code_to_condition(
                weather_code
            )
        )


        return {

            "success": True,

            "latitude": float(lat),

            "longitude": float(lon),

            "observations": {

                "wind_speed":
                    safe_json_value(
                        wind_speed
                    ),

                "wave_height":
                    safe_json_value(
                        wave_height
                    ),

                "rainfall":
                    safe_json_value(
                        rainfall
                    ),

                "weather_code":
                    safe_json_value(
                        weather_code
                    ),

                "weather_condition":
                    weather_condition
            },

            "units": {

                "wind_speed":
                    "km/h",

                "wave_height":
                    "m",

                "rainfall":
                    "mm"
            },

            "source":
                weather_data.get(
                    "source",
                    "Open-Meteo"
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "latitude": float(lat),

            "longitude": float(lon),

            "error":
                str(exc)

        }


# ============================================================
# FISH
# ============================================================

def run_fish_agent(
    species: str = DEFAULT_SPECIES,
    temperature: Any = None,
    chlorophyll: Any = None,
) -> Dict[str, Any]:

    try:

        result = analyze_fish(
            species,
            temperature,
            chlorophyll
        )

        return {

            "success": True,

            "agent": "Fish Agent",

            "inputs": {

                "species":
                    species,

                "temperature":
                    temperature,

                "chlorophyll":
                    chlorophyll
            },

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Fish Agent",

            "error":
                str(exc)
        }


# ============================================================
# OCEAN
# ============================================================

def run_ocean_agent(
    temperature: Any = None,
    chlorophyll: Any = None,
    salinity: float = DEFAULT_SALINITY,
) -> Dict[str, Any]:

    try:

        result = analyze_ocean(
            temperature,
            chlorophyll,
            salinity
        )

        return {

            "success": True,

            "agent":
                "Ocean Agent",

            "inputs": {

                "temperature":
                    temperature,

                "chlorophyll":
                    chlorophyll,

                "salinity":
                    salinity
            },

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Ocean Agent",

            "error":
                str(exc)
        }


# ============================================================
# ECOSYSTEM
# ============================================================

def run_ecosystem_agent(
    fish_risk: str = "Unknown",
    ocean_condition: str = "Unknown",
    temperature: Any = None,
    chlorophyll: Any = None,
) -> Dict[str, Any]:

    try:

        result = analyze_ecosystem(
            fish_risk,
            ocean_condition,
            temperature,
            chlorophyll
        )

        return {

            "success": True,

            "agent":
                "Ecosystem Agent",

            "inputs": {

                "fish_risk":
                    fish_risk,

                "ocean_condition":
                    ocean_condition,

                "temperature":
                    temperature,

                "chlorophyll":
                    chlorophyll
            },

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Ecosystem Agent",

            "error":
                str(exc)
        }


# ============================================================
# WEATHER AGENT
# ============================================================

def run_weather_agent(
    wind_speed: Any = 0,
    wave_height: Any = 0,
    rainfall: Any = 0,
    weather_condition: str = "Unknown",
) -> Dict[str, Any]:

    try:

        result = analyze_weather(
            wind_speed or 0,
            wave_height or 0,
            rainfall or 0,
            weather_condition
        )

        return {

            "success": True,

            "agent":
                "Weather Agent",

            "inputs": {

                "wind_speed":
                    wind_speed,

                "wave_height":
                    wave_height,

                "rainfall":
                    rainfall,

                "weather_condition":
                    weather_condition
            },

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Weather Agent",

            "error":
                str(exc)
        }


# ============================================================
# RISK
# ============================================================

def run_risk_agent(
    fish_risk: str = "Unknown",
    ocean_condition: str = "Unknown",
    ecosystem_status: str = "Unknown",
) -> Dict[str, Any]:

    try:

        result = calculate_risk(
            fish_risk,
            ocean_condition,
            ecosystem_status
        )

        return {

            "success": True,

            "agent":
                "Risk Agent",

            "inputs": {

                "fish_risk":
                    fish_risk,

                "ocean_condition":
                    ocean_condition,

                "ecosystem_status":
                    ecosystem_status
            },

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Risk Agent",

            "error":
                str(exc)
        }


# ============================================================
# EVIDENCE
# ============================================================

def run_evidence_agent(
    species: str = DEFAULT_SPECIES,
    temperature: Any = None,
    chlorophyll: Any = None,
    salinity: Any = DEFAULT_SALINITY,
) -> Dict[str, Any]:

    try:

        result = find_evidence(
            species,
            temperature,
            chlorophyll,
            salinity
        )

        return {

            "success": True,

            "agent":
                "Evidence Agent",

            "inputs": {

                "species":
                    species,

                "temperature":
                    temperature,

                "chlorophyll":
                    chlorophyll,

                "salinity":
                    salinity
            },

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Evidence Agent",

            "error":
                str(exc)
        }


# ============================================================
# UNCERTAINTY
# ============================================================

def run_uncertainty_agent(
    temperature: Any = None,
    chlorophyll: Any = None,
    salinity: Any = DEFAULT_SALINITY,
) -> Dict[str, Any]:

    try:

        result = calculate_uncertainty(
            temperature,
            chlorophyll,
            salinity
        )

        return {

            "success": True,

            "agent":
                "Uncertainty Agent",

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Uncertainty Agent",

            "error":
                str(exc)
        }


# ============================================================
# REASONING
# ============================================================

def run_reasoning_agent(
    species: str = DEFAULT_SPECIES,
    temperature: Any = None,
    chlorophyll: Any = None,
    salinity: Any = DEFAULT_SALINITY,
    fish_result: Dict[str, Any] | None = None,
    ocean_result: Dict[str, Any] | None = None,
    ecosystem_result: Dict[str, Any] | None = None,
    risk_result: Dict[str, Any] | None = None,
) -> Dict[str, Any]:

    try:

        result = generate_reasoning(

            species,

            temperature,

            chlorophyll,

            salinity,

            fish_result or {},

            ocean_result or {},

            ecosystem_result or {},

            risk_result or {}
        )

        return {

            "success": True,

            "agent":
                "Reasoning Agent",

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Reasoning Agent",

            "error":
                str(exc)
        }


# ============================================================
# CAUSAL
# ============================================================

def run_causal_agent(
    temperature: Any = None,
    chlorophyll: Any = None,
    salinity: Any = DEFAULT_SALINITY,
    fish_risk: str = "Unknown",
    ocean_condition: str = "Unknown",
) -> Dict[str, Any]:

    try:

        result = build_causal_chain(

            temperature=
                temperature,

            chlorophyll=
                chlorophyll,

            salinity=
                salinity,

            fish_risk=
                fish_risk,

            ocean_condition=
                ocean_condition
        )

        return {

            "success": True,

            "agent":
                "Causal Reasoning Agent",

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Causal Reasoning Agent",

            "error":
                str(exc)
        }


# ============================================================
# DEBATE
# ============================================================

def run_debate_agent(
    fish_result: Dict[str, Any] | None = None,
    ocean_result: Dict[str, Any] | None = None,
    ecosystem_result: Dict[str, Any] | None = None,
) -> Dict[str, Any]:

    try:

        result = analyze_agent_disagreement(

            fish_result or {},

            ocean_result or {},

            ecosystem_result or {}
        )

        return {

            "success": True,

            "agent":
                "Debate Agent",

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Debate Agent",

            "error":
                str(exc)
        }


# ============================================================
# ALERTS
# ============================================================

def run_alert_agent(
    wind_speed: Any = None,
    wave_height: Any = None,
    rainfall: Any = None,
    weather_condition: str = "Unknown",
) -> Dict[str, Any]:

    try:

        result = generate_alerts(

            wind_speed=
                wind_speed,

            wave_height=
                wave_height,

            rainfall=
                rainfall,

            weather_condition=
                weather_condition
        )

        return {

            "success": True,

            "agent":
                "Alert Agent",

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Alert Agent",

            "error":
                str(exc)
        }


# ============================================================
# ROUTE
# ============================================================

def run_route_agent(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    wind_speed: Any = 0,
    wave_height: Any = 0,
    rainfall: Any = 0,
    weather_condition: str = "Unknown",
) -> Dict[str, Any]:

    try:

        result = analyze_route(

            start_lat=
                start_lat,

            start_lon=
                start_lon,

            end_lat=
                end_lat,

            end_lon=
                end_lon,

            wind_speed=
                wind_speed or 0,

            wave_height=
                wave_height or 0,

            rainfall=
                rainfall or 0,

            weather_condition=
                weather_condition
        )

        return {

            "success": True,

            "agent":
                "Route Agent",

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Route Agent",

            "error":
                str(exc)
        }


# ============================================================
# GEOFENCE
# ============================================================

def run_geofence_agent(
    route_points: list,
    restricted_zones: list,
) -> Dict[str, Any]:

    try:

        result = analyze_geofence(

            route_points=
                route_points,

            restricted_zones=
                restricted_zones
        )

        return {

            "success": True,

            "agent":
                "Geofence Agent",

            "result":
                safe_json_value(
                    result
                )
        }


    except Exception as exc:

        return {

            "success": False,

            "agent":
                "Geofence Agent",

            "error":
                str(exc)
        }


# ============================================================
# TOOL REGISTRY
# ============================================================

TOOL_FUNCTIONS = {

    "get_marine_observations":
        get_marine_observations,

    "get_marine_weather":
        get_marine_weather,

    "run_fish_agent":
        run_fish_agent,

    "run_ocean_agent":
        run_ocean_agent,

    "run_ecosystem_agent":
        run_ecosystem_agent,

    "run_weather_agent":
        run_weather_agent,

    "run_risk_agent":
        run_risk_agent,

    "run_evidence_agent":
        run_evidence_agent,

    "run_uncertainty_agent":
        run_uncertainty_agent,

    "run_reasoning_agent":
        run_reasoning_agent,

    "run_causal_agent":
        run_causal_agent,

    "run_debate_agent":
        run_debate_agent,

    "run_alert_agent":
        run_alert_agent,

    "run_route_agent":
        run_route_agent,

    "run_geofence_agent":
        run_geofence_agent,
}


# ============================================================
# GEMINI TOOL DECLARATIONS
# ============================================================

GEMINI_ORCA_TOOLS = [

    {
        "type": "function",

        "name":
            "get_marine_observations",

        "description":
            "Retrieve real marine observations for the "
            "trusted ORCA location and date.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "lat": {
                    "type": "number"
                },

                "lon": {
                    "type": "number"
                },

                "date": {
                    "type": "string"
                }
            },

            "required": [
                "lat",
                "lon",
                "date"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "get_marine_weather",

        "description":
            "Retrieve marine weather observations for "
            "the requested ORCA location.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "lat": {
                    "type": "number"
                },

                "lon": {
                    "type": "number"
                }
            },

            "required": [
                "lat",
                "lon"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "run_fish_agent",

        "description":
            "Run the Fish Agent using already retrieved "
            "ORCA marine observations.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "species": {
                    "type": "string"
                },

                "temperature": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "chlorophyll": {
                    "type": [
                        "number",
                        "null"
                    ]
                }
            },

            "required": [
                "species",
                "temperature",
                "chlorophyll"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "run_ocean_agent",

        "description":
            "Run Ocean Agent using marine observations "
            "and ORCA salinity.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "temperature": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "chlorophyll": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "salinity": {
                    "type":
                        "number"
                }
            },

            "required": [
                "temperature",
                "chlorophyll",
                "salinity"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "run_ecosystem_agent",

        "description":
            "Run Ecosystem Agent using actual Fish Agent "
            "and Ocean Agent results.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "fish_risk": {
                    "type":
                        "string"
                },

                "ocean_condition": {
                    "type":
                        "string"
                },

                "temperature": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "chlorophyll": {
                    "type": [
                        "number",
                        "null"
                    ]
                }
            },

            "required": [
                "fish_risk",
                "ocean_condition",
                "temperature",
                "chlorophyll"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "run_weather_agent",

        "description":
            "Run Weather Agent using actual weather tool "
            "observations.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "wind_speed": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "wave_height": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "rainfall": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "weather_condition": {
                    "type":
                        "string"
                }
            },

            "required": [
                "wind_speed",
                "wave_height",
                "rainfall",
                "weather_condition"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "run_evidence_agent",

        "description":
            "Run Evidence Agent using actual marine "
            "observations and ORCA species context.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "species": {
                    "type":
                        "string"
                },

                "temperature": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "chlorophyll": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "salinity": {
                    "type": [
                        "number",
                        "null"
                    ]
                }
            },

            "required": [
                "species",
                "temperature",
                "chlorophyll",
                "salinity"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "run_uncertainty_agent",

        "description":
            "Run uncertainty analysis using actual "
            "marine observations.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "temperature": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "chlorophyll": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "salinity": {
                    "type": [
                        "number",
                        "null"
                    ]
                }
            },

            "required": [
                "temperature",
                "chlorophyll",
                "salinity"
            ]
        }
    },


    {
        "type": "function",

        "name":
            "run_causal_agent",

        "description":
            "Build an evidence-informed causal pathway "
            "from actual specialist results.",

        "parameters": {

            "type":
                "object",

            "properties": {

                "temperature": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "chlorophyll": {
                    "type": [
                        "number",
                        "null"
                    ]
                },

                "salinity": {
                    "type":
                        "number"
                },

                "fish_risk": {
                    "type":
                        "string"
                },

                "ocean_condition": {
                    "type":
                        "string"
                }
            },

            "required": [
                "temperature",
                "chlorophyll",
                "salinity",
                "fish_risk",
                "ocean_condition"
            ]
        }
    }
]


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool_call(
    name: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:

    if name not in TOOL_FUNCTIONS:

        return {

            "success":
                False,

            "error":
                f"Unknown ORCA tool: {name}"
        }


    function = TOOL_FUNCTIONS[
        name
    ]


    try:

        result = function(
            **(arguments or {})
        )

        return safe_json_value(
            result
        )


    except Exception as exc:

        return {

            "success":
                False,

            "tool":
                name,

            "error":
                str(exc)
        }


# ============================================================
# TOOL NAMES
# ============================================================

def available_tool_names():

    return list(
        TOOL_FUNCTIONS.keys()
    )

# ============================================================
# ORCA - FASTAPI BACKEND
# ============================================================

from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data.weather_data import get_weather_data

from agents.orca_controller import (
    run_orca,
    run_orca_with_location,
    run_spatial_pfz,
    run_geofence_analysis,
    run_safety_decision,
    run_route_analysis,
    run_alert_analysis,
    run_orca_chat,
    run_agentic_orca,
)

from agents.llm_orchestrator import (
    run_agentic_llm,
    get_orchestrator_status,
)

from agents.ecosystem_agent import analyze_ecosystem
from agents.risk_agent import calculate_risk
from agents.ocean_agent import analyze_ocean
from agents.weather_agent import analyze_weather
from agents.route_agent import analyze_route


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="ORCA",
    description="Ocean Reasoning with Collaborative Agents",
    version="2.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DEFAULT VALUES
# ============================================================

DEFAULT_SPECIES = "Indian Oil Sardine"
DEFAULT_LAT = 9.5
DEFAULT_LON = 76.0
DEFAULT_DATE = "2020-05-01"
DEFAULT_SALINITY = 34.0


# ============================================================
# HELPERS
# ============================================================

def safe_value(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, dict):
        return {
            str(k): safe_value(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [safe_value(v) for v in value]

    try:
        return value.item()
    except Exception:
        return str(value)


def weather_code_to_condition(weather_code) -> str:
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


def find_tool_result(
    tool_calls: List[Dict[str, Any]],
    tool_name: str,
) -> Dict[str, Any]:

    for item in reversed(tool_calls):

        if item.get("tool") != tool_name:
            continue

        result = item.get(
            "result",
            {}
        )

        if not isinstance(result, dict):
            return {}

        nested = result.get("result")

        if isinstance(nested, dict):
            return nested

        return result

    return {}


def build_agentic_response(
    llm_result: Dict[str, Any],
    query: str,
    species: str,
    lat: float,
    lon: float,
    date: str,
    salinity: float,
) -> Dict[str, Any]:

    tool_calls = llm_result.get(
        "tool_calls",
        []
    )

    marine = find_tool_result(
        tool_calls,
        "get_marine_observations"
    )

    weather = find_tool_result(
        tool_calls,
        "get_marine_weather"
    )

    fish = find_tool_result(
        tool_calls,
        "run_fish_agent"
    )

    ocean = find_tool_result(
        tool_calls,
        "run_ocean_agent"
    )

    ecosystem = find_tool_result(
        tool_calls,
        "run_ecosystem_agent"
    )

    risk = find_tool_result(
        tool_calls,
        "run_risk_agent"
    )

    evidence = find_tool_result(
        tool_calls,
        "run_evidence_agent"
    )

    uncertainty = find_tool_result(
        tool_calls,
        "run_uncertainty_agent"
    )

    causal = find_tool_result(
        tool_calls,
        "run_causal_agent"
    )

    reasoning = find_tool_result(
        tool_calls,
        "run_reasoning_agent"
    )

    debate = find_tool_result(
        tool_calls,
        "run_debate_agent"
    )

    alerts = find_tool_result(
        tool_calls,
        "run_alert_agent"
    )

    weather_analysis = find_tool_result(
        tool_calls,
        "run_weather_agent"
    )

    observations = (
        marine.get(
            "observations",
            {}
        )
        if marine
        else {}
    )

    sources = (
        marine.get(
            "sources",
            {}
        )
        if marine
        else {}
    )

    overall_risk = risk.get(
        "overall_risk",
        fish.get(
            "risk",
            "Unknown"
        )
    )

    return {

        "project":
            "ORCA",

        "query":
            query,

        "species":
            species,

        "location": {

            "latitude":
                lat,

            "longitude":
                lon,
        },

        "date":
            date,

        "observations":
            observations,

        "marine_observations":
            marine,

        "weather_analysis":
            weather_analysis,

        "weather":
            weather,

        "fish_analysis":
            fish,

        "ocean_analysis":
            ocean,

        "ecosystem_analysis":
            ecosystem,

        "risk_analysis":
            risk,

        "uncertainty_analysis":
            uncertainty,

        "evidence":
            evidence,

        "causal_reasoning":
            causal,

        "reasoning":
            reasoning,

        "agent_debate":
            debate,

        "alerts":
            alerts,

        "decision": {

            "query":
                query,

            "overall_risk":
                overall_risk,

            "decision_ready":
                True,

            "scientific_note":
                (
                    "ORCA provides evidence-informed "
                    "decision support and does not "
                    "replace official marine advisories "
                    "or professional judgment."
                ),
        },

        "llm": {

            "enabled":
                llm_result.get(
                    "llm_used",
                    False
                ),

            "model":
                llm_result.get(
                    "model"
                ),

            "answer":
                llm_result.get(
                    "answer",
                    ""
                ),

            "key_findings":
                llm_result.get(
                    "key_findings",
                    []
                ),

            "recommendation":
                llm_result.get(
                    "recommendation",
                    ""
                ),

            "uncertainty":
                llm_result.get(
                    "uncertainty",
                    ""
                ),

            "sources_used":
                llm_result.get(
                    "sources_used",
                    []
                ),

            "rounds":
                llm_result.get(
                    "rounds",
                    0
                ),
        },

        "llm_orchestration": {

            "enabled":
                True,

            "model":
                llm_result.get(
                    "model"
                ),

            "agentic_loop_used":
                llm_result.get(
                    "llm_used",
                    False
                ),

            "tool_call_count":
                len(tool_calls),

            "trusted_context":
                llm_result.get(
                    "trusted_context",
                    {}
                ),
        },

        "tool_calls":
            tool_calls,

        "data_sources": {

            "marine":
                sources,

            "weather":
                (
                    weather.get(
                        "source",
                        "Open-Meteo"
                    )
                    if weather
                    else "Open-Meteo"
                ),
        },

        "system_status":
            (
                "Agentic ORCA analysis completed"
                if llm_result.get(
                    "success",
                    False
                )
                else
                "Agentic ORCA analysis failed"
            ),

        "llm_error":
            llm_result.get(
                "error"
            ),
    }


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {

        "project":
            "ORCA",

        "message":
            (
                "ORCA Marine Ecosystem Intelligence "
                "System is running"
            ),

        "version":
            "2.0.0",

        "llm_enabled":
            True,
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {

        "status":
            "healthy",

        "system":
            "ORCA",

        "llm":
            get_orchestrator_status(),
    }


# ============================================================
# LLM STATUS
# ============================================================

@app.get("/llm-status")
def llm_status():

    return get_orchestrator_status()


# ============================================================
# FISH ANALYSIS
# ============================================================

@app.get("/fish-analysis")
def fish_analysis(
    species: str,
    temperature: float,
    chlorophyll: float
):

    return run_orca(
        species,
        temperature,
        chlorophyll,
        DEFAULT_SALINITY
    )[
        "fish_analysis"
    ]


# ============================================================
# OCEAN ANALYSIS
# ============================================================

@app.get("/ocean-analysis")
def ocean_analysis(
    temperature: float,
    chlorophyll: float,
    salinity: float
):

    return run_orca(
        DEFAULT_SPECIES,
        temperature,
        chlorophyll,
        salinity
    )[
        "ocean_analysis"
    ]


# ============================================================
# ECOSYSTEM ANALYSIS
# ============================================================

@app.get("/ecosystem-analysis")
def ecosystem_analysis(
    fish_risk: str,
    ocean_condition: str,
    temperature: float,
    chlorophyll: float
):

    return analyze_ecosystem(
        fish_risk,
        ocean_condition,
        temperature,
        chlorophyll
    )


# ============================================================
# RISK ANALYSIS
# ============================================================

@app.get("/risk-analysis")
def risk_analysis(
    fish_risk: str,
    ocean_condition: str,
    ecosystem_status: str
):

    return calculate_risk(
        fish_risk,
        ocean_condition,
        ecosystem_status
    )


# ============================================================
# COMPLETE ORCA ANALYSIS
# ============================================================

@app.get("/orca-analysis")
def orca_analysis(
    species: str,
    temperature: float,
    chlorophyll: float,
    salinity: float
):

    return run_orca(
        species,
        temperature,
        chlorophyll,
        salinity
    )


# ============================================================
# LOCATION ORCA ANALYSIS
# ============================================================

@app.get("/orca-location-analysis")
def orca_location_analysis(
    species: str,
    lat: float,
    lon: float,
    date: str,
    salinity: float = DEFAULT_SALINITY
):

    return run_orca_with_location(
        species,
        lat,
        lon,
        date,
        salinity
    )


# ============================================================
# CHAT
# ============================================================

@app.get("/chat")
def chat(
    query: str,
    species: str = DEFAULT_SPECIES,
    temperature: float = 30,
    chlorophyll: float = 0.3,
    salinity: float = DEFAULT_SALINITY,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON
):

    return run_orca_chat(
        query=query,
        species=species,
        temperature=temperature,
        chlorophyll=chlorophyll,
        salinity=salinity,
        lat=lat,
        lon=lon
    )


# ============================================================
# AGENTIC ORCA
#
# Gemini first.
# Deterministic ORCA fallback when Gemini is unavailable,
# rate-limited or returns an unsuccessful result.
# ============================================================

@app.get("/agentic-orca")
def agentic_orca(
    query: str,
    species: str = DEFAULT_SPECIES,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    date: str = DEFAULT_DATE,
    salinity: float = DEFAULT_SALINITY
):

    print(
        "\n================================================"
    )

    print(
        "FASTAPI /agentic-orca REQUEST"
    )

    print(
        "================================================"
    )

    print(
        f"Query: {query}"
    )

    print(
        f"Species: {species}"
    )

    print(
        f"Latitude: {lat}"
    )

    print(
        f"Longitude: {lon}"
    )

    print(
        f"Date: {date}"
    )

    print(
        f"Salinity: {salinity}"
    )


    # ========================================================
    # GEMINI
    # ========================================================

    llm_result = None

    try:

        llm_result = run_agentic_llm(

            query=query,

            lat=lat,

            lon=lon,

            date=date,

            salinity=salinity,

            species=species
        )


        if (
            isinstance(
                llm_result,
                dict
            )
            and llm_result.get(
                "success"
            )
            and llm_result.get(
                "llm_used"
            )
        ):

            print(
                "Gemini agentic analysis succeeded."
            )

            return build_agentic_response(

                llm_result=
                    llm_result,

                query=
                    query,

                species=
                    species,

                lat=
                    lat,

                lon=
                    lon,

                date=
                    date,

                salinity=
                    salinity
            )


        print(
            "Gemini unavailable. "
            "Activating deterministic ORCA fallback."
        )


        if isinstance(
            llm_result,
            dict
        ):

            print(
                "LLM error:",
                llm_result.get(
                    "error"
                )
            )


    except Exception as exc:

        print(
            "Gemini orchestration exception:",
            repr(exc)
        )


    # ========================================================
    # DETERMINISTIC FALLBACK
    # ========================================================

    try:

        fallback = run_agentic_orca(

            query=query,

            species=species,

            lat=lat,

            lon=lon,

            date=date,

            salinity=salinity
        )


        fallback = safe_value(
            fallback
        )


        if not isinstance(
            fallback,
            dict
        ):

            fallback = {}


        fallback[
            "llm_fallback"
        ] = True


        fallback[
            "llm_fallback_reason"
        ] = (
            "Gemini was unavailable or rate-limited. "
            "ORCA completed the assessment using the "
            "deterministic specialist-agent pipeline."
        )


        fallback[
            "requested_date"
        ] = date


        fallback[
            "requested_location"
        ] = {

            "latitude":
                lat,

            "longitude":
                lon,
        }


        fallback[
            "llm_error"
        ] = (
            llm_result.get(
                "error"
            )
            if isinstance(
                llm_result,
                dict
            )
            else None
        )


        return fallback


    except Exception as exc:

        print(
            "Deterministic ORCA fallback error:",
            repr(exc)
        )


        return {

            "project":
                "ORCA",

            "status":
                "error",

            "query":
                query,

            "species":
                species,

            "location": {

                "latitude":
                    lat,

                "longitude":
                    lon,
            },

            "date":
                date,

            "llm_fallback":
                True,

            "llm_fallback_reason":
                (
                    "Both Gemini orchestration and "
                    "deterministic ORCA execution failed."
                ),

            "error":
                str(exc),

            "system_status":
                "ORCA analysis failed",
        }


# ============================================================
# SPATIAL PFZ
# ============================================================

@app.get("/spatial-pfz")
def spatial_pfz(
    min_lat: float = 9.0,
    max_lat: float = 9.4,
    min_lon: float = 75.6,
    max_lon: float = 76.4,
    date: str = DEFAULT_DATE
):

    return run_spatial_pfz(
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        date
    )


# ============================================================
# PFZ MAP
# ============================================================

@app.get("/pfz-map")
def pfz_map(
    min_lat: float = 9.0,
    max_lat: float = 9.4,
    min_lon: float = 75.6,
    max_lon: float = 76.4,
    date: str = DEFAULT_DATE
):

    return run_spatial_pfz(
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        date
    )


# ============================================================
# GEOFENCE
# ============================================================

@app.get("/geofence")
def geofence(
    lat: float,
    lon: float
):

    route_points = [
        [lat, lon]
    ]

    restricted_zones = []

    return run_geofence_analysis(
        route_points,
        restricted_zones
    )


# ============================================================
# SAFETY DECISION
# ============================================================

@app.get("/safety-decision")
def safety_decision(
    query: str = "Marine safety assessment",
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    wind_speed: float = 0,
    wave_height: float = 0,
    rainfall: float = 0,
    weather_condition: str = "Unknown"
):

    return run_safety_decision(
        query=query,
        lat=lat,
        lon=lon,
        wind_speed=wind_speed,
        wave_height=wave_height,
        rainfall=rainfall,
        weather_condition=weather_condition
    )


# ============================================================
# SAFE ROUTE
# ============================================================

@app.get("/safe-route")
def safe_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):

    return run_route_analysis(
        start_lat=start_lat,
        start_lon=start_lon,
        end_lat=end_lat,
        end_lon=end_lon
    )


# ============================================================
# ALERTS
# ============================================================

@app.get("/alerts")
def alerts(
    query: str,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON
):

    try:

        weather_result = get_weather_data(
            lat,
            lon
        )


        wind_speed = weather_result.get(
            "wind_speed"
        )

        wave_height = weather_result.get(
            "wave_height"
        )

        rainfall = weather_result.get(
            "rainfall"
        )

        weather_condition = weather_result.get(
            "weather_condition"
        )


        if not weather_condition:

            weather_condition = (
                weather_code_to_condition(
                    weather_result.get(
                        "weather_code"
                    )
                )
            )


        return run_alert_analysis(

            query=query,

            lat=lat,

            lon=lon,

            wind_speed=wind_speed,

            wave_height=wave_height,

            rainfall=rainfall,

            weather_condition=weather_condition
        )


    except Exception as exc:

        return {

            "status":
                "error",

            "message":
                "Marine alert analysis failed",

            "error":
                str(exc)
        }


# ============================================================
# OCEAN LOCATION ANALYSIS
# ============================================================

@app.get("/ocean-location-analysis")
def ocean_location_analysis(
    lat: float,
    lon: float,
    date: str,
    salinity: float = DEFAULT_SALINITY
):

    from data.marine_data import (
        get_marine_data
    )


    marine_data = get_marine_data(
        lat,
        lon,
        date
    )


    temperature = None

    chlorophyll = None


    try:

        sst_rows = (

            marine_data[
                "sst"
            ][
                "data"
            ][
                "table"
            ][
                "rows"
            ]
        )


        if sst_rows:

            temperature = float(
                sst_rows[0][-1]
            )


    except Exception:

        temperature = None


    try:

        chl_rows = (

            marine_data[
                "chlorophyll"
            ][
                "data"
            ][
                "table"
            ][
                "rows"
            ]
        )


        if chl_rows:

            chlorophyll = float(
                chl_rows[0][-1]
            )


    except Exception:

        chlorophyll = None


    ocean_result = analyze_ocean(

        temperature,

        chlorophyll,

        salinity
    )


    return {

        "project":
            "ORCA",

        "location": {

            "latitude":
                lat,

            "longitude":
                lon
        },

        "date":
            date,

        "data_sources": {

            "sst":
                "NOAA CoastWatch MUR SST",

            "chlorophyll":
                "INCOIS Oceansat-2 OCM"
        },

        "observations": {

            "sea_surface_temperature":
                temperature,

            "chlorophyll":
                chlorophyll,

            "salinity":
                salinity
        },

        "ocean_analysis":
            ocean_result,

        "historical_data_note":
            (
                "The requested date determines whether "
                "the observation is historical or recent. "
                "ORCA does not automatically label historical "
                "observations as current."
            )
    }


# ============================================================
# WEATHER LOCATION ANALYSIS
# ============================================================

@app.get("/weather-location-analysis")
def weather_location_analysis(
    lat: float,
    lon: float
):

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


    weather_analysis = analyze_weather(

        wind_speed
        if wind_speed is not None
        else 0,

        wave_height
        if wave_height is not None
        else 0,

        rainfall
        if rainfall is not None
        else 0,

        weather_condition
    )


    return {

        "project":
            "ORCA",

        "location": {

            "latitude":
                lat,

            "longitude":
                lon
        },

        "source":
            weather_data.get(
                "source",
                "Open-Meteo"
            ),

        "weather": {

            "wind_speed":
                wind_speed,

            "wave_height":
                wave_height,

            "rainfall":
                rainfall,

            "weather_code":
                weather_code,

            "weather_condition":
                weather_condition
        },

        "analysis":
            weather_analysis,

        "scientific_note":
            (
                "ORCA uses weather and marine "
                "conditions for decision support. "
                "This does not replace official "
                "marine safety advisories."
            )
    }


# ============================================================
# ROUTE ANALYSIS
# ============================================================

@app.get("/route-analysis")
def route_analysis(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):

    weather_data = get_weather_data(
        start_lat,
        start_lon
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


    route_result = analyze_route(

        start_lat=start_lat,

        start_lon=start_lon,

        end_lat=end_lat,

        end_lon=end_lon,

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

        "project":
            "ORCA",

        "route_analysis":
            route_result,

        "weather_source":
            weather_data.get(
                "source",
                "Open-Meteo"
            ),

        "weather": {

            "wind_speed":
                wind_speed,

            "wave_height":
                wave_height,

            "rainfall":
                rainfall,

            "weather_condition":
                weather_condition
        },

        "scientific_note":
            (
                "ORCA evaluates route safety using "
                "available marine weather conditions. "
                "The result is decision support and "
                "does not guarantee safe navigation."
            )
    }


# ============================================================
# RUN
# ============================================================

# Start with:
#
# python -m uvicorn main:app --host 127.0.0.1 --port 8001
#
# ============================================================

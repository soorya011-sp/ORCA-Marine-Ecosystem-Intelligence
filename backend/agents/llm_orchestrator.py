# ============================================================
# ORCA - GEMINI LLM ORCHESTRATOR
# ============================================================

import ast
import json
import os
import re
from typing import Any, Dict, List

from dotenv import load_dotenv
from google import genai

from agents.llm_agent_tools import (
    GEMINI_ORCA_TOOLS,
    TOOL_FUNCTIONS,
    execute_tool_call,
    get_marine_observations,
    get_marine_weather,
    run_fish_agent,
    run_ocean_agent,
    run_ecosystem_agent,
    run_weather_agent,
    run_risk_agent,
    run_evidence_agent,
    run_uncertainty_agent,
    run_reasoning_agent,
    run_causal_agent,
    run_debate_agent,
    run_alert_agent,
    run_route_agent,
    run_geofence_agent,
)

# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add GEMINI_API_KEY to backend/.env"
    )

client = genai.Client(api_key=GEMINI_API_KEY)

# ============================================================
# AVAILABLE AGENTS
# ============================================================

AVAILABLE_AGENTS = {
    "fish": "Fish species and productivity analysis.",
    "ocean": "Sea surface temperature, chlorophyll, salinity and ocean analysis.",
    "ecosystem": "Marine ecosystem environmental stress.",
    "weather": "Wind, rainfall, waves and weather.",
    "risk": "Overall environmental risk.",
    "evidence": "Scientific research evidence.",
    "reasoning": "Explainable reasoning.",
    "uncertainty": "Confidence and uncertainty.",
    "debate": "Comparison of specialist opinions.",
    "causal": "Evidence-informed causal pathways.",
    "alerts": "Marine safety alerts.",
    "route": "Marine route safety.",
    "geofence": "Restricted-area analysis.",
    "pfz": "Potential Fishing Zone analysis.",
}

# ============================================================
# HELPERS
# ============================================================

def safe_json_value(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, dict):
        return {
            str(k): safe_json_value(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            safe_json_value(v)
            for v in value
        ]

    try:
        return value.item()
    except Exception:
        return str(value)


def extract_response_text(response: Any) -> str:
    try:
        text = getattr(response, "output_text", None)
        if text:
            return str(text).strip()
    except Exception:
        pass

    try:
        steps = getattr(response, "steps", [])
        collected = []

        for step in steps:
            if getattr(step, "type", "") != "model_output":
                continue

            content = getattr(step, "content", None)
            if not content:
                continue

            for block in content:
                block_text = getattr(block, "text", None)
                if block_text:
                    collected.append(str(block_text))

        if collected:
            return "\n".join(collected).strip()
    except Exception:
        pass

    try:
        text = getattr(response, "text", None)
        if text:
            return str(text).strip()
    except Exception:
        pass

    return ""


def parse_json_object(text: str) -> Dict[str, Any]:
    if not text:
        raise ValueError("Gemini returned empty text.")

    cleaned = str(text).strip()

    cleaned = re.sub(
        r"^```(?:json|python)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    ).strip()

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start >= 0 and end > start:
        candidate = cleaned[start:end + 1]

        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        try:
            parsed = ast.literal_eval(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

    try:
        parsed = ast.literal_eval(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    raise ValueError(
        "Unable to parse Gemini response.\n"
        f"Raw response:\n{cleaned}"
    )


# ============================================================
# DETERMINISTIC ROUTING
# ============================================================

def deterministic_routes(query: str) -> List[str]:
    q = query.lower()
    routes: List[str] = []

    keyword_map = {
        "fish": [
            "fish", "sardine", "fishing", "fishery",
            "productivity", "catch", "biomass",
            "species", "stock",
        ],
        "ocean": [
            "ocean", "sea", "sst", "temperature",
            "chlorophyll", "salinity", "marine",
        ],
        "weather": [
            "weather", "wind", "rain", "rainfall",
            "wave", "waves", "storm", "forecast",
            "today", "tomorrow",
        ],
        "route": [
            "route", "navigation", "journey",
            "travel", "safe route",
        ],
        "pfz": [
            "pfz", "potential fishing zone",
            "fishing zone", "fishing area", "hotspot",
        ],
        "geofence": [
            "geofence", "restricted area",
            "restricted zone", "boundary",
        ],
        "evidence": [
            "research", "paper", "study",
            "evidence", "scientific", "literature",
        ],
        "reasoning": [
            "why", "explain", "reason", "how",
        ],
        "causal": [
            "cause", "caused", "because",
            "impact", "effect", "influence",
        ],
        "alerts": [
            "alert", "warning", "hazard",
            "safety warning",
        ],
        "uncertainty": [
            "confidence", "uncertainty",
            "limitation", "limitations",
            "reliable", "reliability",
        ],
        "debate": [
            "disagree", "disagreement",
            "compare agents", "compare opinions",
        ],
    }

    for agent, keywords in keyword_map.items():
        if any(keyword in q for keyword in keywords):
            routes.append(agent)

    if "fish" in routes:
        for agent in [
            "ocean",
            "ecosystem",
            "risk",
            "evidence",
            "reasoning",
            "uncertainty",
            "causal",
        ]:
            if agent not in routes:
                routes.append(agent)

    if "ocean" in routes:
        for agent in [
            "ecosystem",
            "risk",
            "uncertainty",
        ]:
            if agent not in routes:
                routes.append(agent)

    if "weather" in routes:
        for agent in [
            "risk",
            "alerts",
        ]:
            if agent not in routes:
                routes.append(agent)

    if "route" in routes:
        for agent in [
            "weather",
            "risk",
            "alerts",
            "geofence",
        ]:
            if agent not in routes:
                routes.append(agent)

    if "pfz" in routes:
        for agent in [
            "fish",
            "ocean",
            "evidence",
            "uncertainty",
            "risk",
        ]:
            if agent not in routes:
                routes.append(agent)

    if "causal" in routes:
        for agent in [
            "reasoning",
            "evidence",
            "uncertainty",
        ]:
            if agent not in routes:
                routes.append(agent)

    if not routes:
        routes = [
            "fish",
            "ocean",
            "ecosystem",
            "risk",
            "evidence",
            "reasoning",
            "uncertainty",
            "causal",
        ]

    return routes


# ============================================================
# PLANNING
# ============================================================

def build_planning_prompt(query: str) -> str:
    return f"""
You are ORCA's intelligent planning layer.

USER QUESTION:
{query}

AVAILABLE AGENTS:
{json.dumps(AVAILABLE_AGENTS, indent=2)}

Choose the relevant specialist agents.

Return ONLY JSON:

{{
  "intent": "string",
  "complexity": "simple|moderate|complex",
  "selected_agents": [],
  "reason": "short explanation",
  "requires_marine_data": true,
  "requires_weather_data": false,
  "requires_research_evidence": true
}}
"""


def normalize_plan(
    plan: Dict[str, Any],
    query: str
) -> Dict[str, Any]:

    if not isinstance(plan, dict):
        plan = {}

    selected: List[str] = []

    llm_agents = plan.get("selected_agents", [])

    if isinstance(llm_agents, list):
        for agent in llm_agents:
            name = str(agent).strip().lower()

            if (
                name in AVAILABLE_AGENTS
                and name not in selected
            ):
                selected.append(name)

    for agent in deterministic_routes(query):
        if agent not in selected:
            selected.append(agent)

    return {
        "intent": str(
            plan.get(
                "intent",
                "Marine ecosystem analysis"
            )
        ),
        "complexity": str(
            plan.get(
                "complexity",
                "moderate"
            )
        ),
        "selected_agents": selected,
        "reason": str(
            plan.get(
                "reason",
                "Relevant ORCA agents selected."
            )
        ),
        "requires_marine_data": bool(
            plan.get(
                "requires_marine_data",
                True
            )
        ),
        "requires_weather_data": bool(
            plan.get(
                "requires_weather_data",
                "weather" in selected or "route" in selected
            )
        ),
        "requires_research_evidence": bool(
            plan.get(
                "requires_research_evidence",
                "evidence" in selected
            )
        ),
    }


def plan_with_llm(query: str) -> Dict[str, Any]:
    print("LLM planning started...")

    try:
        response = client.interactions.create(
            model=GEMINI_MODEL,
            input=build_planning_prompt(query),
        )

        text = extract_response_text(response)

        print("LLM planning response received.")
        print("LLM planning raw text:")
        print(text)

        result = normalize_plan(
            parse_json_object(text),
            query,
        )

        result["llm_planning_failed"] = False
        result["llm_used"] = True

        return result

    except Exception as exc:
        print(
            "LLM planning error:",
            repr(exc),
        )

        fallback = normalize_plan(
            {},
            query,
        )

        fallback["llm_planning_failed"] = True
        fallback["llm_used"] = False
        fallback["llm_error"] = str(exc)
        fallback["reason"] = (
            "Deterministic ORCA planning was used "
            "because the LLM planning layer was unavailable."
        )

        return fallback


# ============================================================
# TRUSTED CONTEXT
# ============================================================

def build_trusted_context(
    query: str,
    lat: float,
    lon: float,
    date: str,
    salinity: float,
    species: str,
) -> Dict[str, Any]:

    return {
        "query": query,
        "latitude": float(lat),
        "longitude": float(lon),
        "observation_date": str(date),
        "salinity": float(salinity),
        "species": str(species),
    }


# ============================================================
# STATE
# ============================================================

def create_state(
    context: Dict[str, Any]
) -> Dict[str, Any]:

    return {
        "context": context,
        "marine": None,
        "weather": None,
        "fish": None,
        "ocean": None,
        "ecosystem": None,
        "weather_analysis": None,
        "evidence": None,
        "uncertainty": None,
        "causal": None,
        "risk": None,
        "reasoning": None,
        "debate": None,
        "alerts": None,
        "route": None,
        "geofence": None,
        "tool_history": [],
    }


def unwrap_result(
    value: Any
) -> Dict[str, Any]:

    if not isinstance(value, dict):
        return {}

    nested = value.get("result")

    if isinstance(nested, dict):
        return nested

    return value


# ============================================================
# TRUSTED ARGUMENT ENFORCEMENT
# ============================================================

def enforce_state(
    name: str,
    arguments: Dict[str, Any],
    state: Dict[str, Any],
) -> Dict[str, Any]:

    args = dict(arguments or {})
    context = state["context"]

    if name == "get_marine_observations":
        args["lat"] = context["latitude"]
        args["lon"] = context["longitude"]
        args["date"] = context["observation_date"]

    elif name == "get_marine_weather":
        args["lat"] = context["latitude"]
        args["lon"] = context["longitude"]

    elif name == "run_fish_agent":
        args["species"] = context["species"]

        marine = state.get("marine")

        if marine:
            obs = marine.get("observations", {})

            args["temperature"] = obs.get(
                "sea_surface_temperature"
            )

            args["chlorophyll"] = obs.get(
                "chlorophyll"
            )

    elif name == "run_ocean_agent":
        args["salinity"] = context["salinity"]

        marine = state.get("marine")

        if marine:
            obs = marine.get("observations", {})

            args["temperature"] = obs.get(
                "sea_surface_temperature"
            )

            args["chlorophyll"] = obs.get(
                "chlorophyll"
            )

    elif name == "run_evidence_agent":
        args["species"] = context["species"]
        args["salinity"] = context["salinity"]

        marine = state.get("marine")

        if marine:
            obs = marine.get("observations", {})

            args["temperature"] = obs.get(
                "sea_surface_temperature"
            )

            args["chlorophyll"] = obs.get(
                "chlorophyll"
            )

    elif name == "run_uncertainty_agent":
        args["salinity"] = context["salinity"]

        marine = state.get("marine")

        if marine:
            obs = marine.get("observations", {})

            args["temperature"] = obs.get(
                "sea_surface_temperature"
            )

            args["chlorophyll"] = obs.get(
                "chlorophyll"
            )

    elif name == "run_weather_agent":
        weather = state.get("weather")

        if weather:
            obs = weather.get("observations", {})

            args["wind_speed"] = obs.get(
                "wind_speed"
            )

            args["wave_height"] = obs.get(
                "wave_height"
            )

            args["rainfall"] = obs.get(
                "rainfall"
            )

            args["weather_condition"] = obs.get(
                "weather_condition",
                "Unknown",
            )

    elif name == "run_ecosystem_agent":
        fish = unwrap_result(
            state.get("fish") or {}
        )

        ocean = unwrap_result(
            state.get("ocean") or {}
        )

        marine = state.get("marine")

        args["fish_risk"] = fish.get(
            "risk",
            "Unknown",
        )

        args["ocean_condition"] = ocean.get(
            "ocean_condition",
            "Unknown",
        )

        if marine:
            obs = marine.get("observations", {})

            args["temperature"] = obs.get(
                "sea_surface_temperature"
            )

            args["chlorophyll"] = obs.get(
                "chlorophyll"
            )

    elif name == "run_risk_agent":
        fish = unwrap_result(
            state.get("fish") or {}
        )

        ocean = unwrap_result(
            state.get("ocean") or {}
        )

        ecosystem = unwrap_result(
            state.get("ecosystem") or {}
        )

        args["fish_risk"] = fish.get(
            "risk",
            "Unknown",
        )

        args["ocean_condition"] = ocean.get(
            "ocean_condition",
            "Unknown",
        )

        args["ecosystem_status"] = ecosystem.get(
            "ecosystem_status",
            "Unknown",
        )

    elif name == "run_causal_agent":
        args["salinity"] = context["salinity"]

        fish = unwrap_result(
            state.get("fish") or {}
        )

        ocean = unwrap_result(
            state.get("ocean") or {}
        )

        marine = state.get("marine")

        args["fish_risk"] = fish.get(
            "risk",
            "Unknown",
        )

        args["ocean_condition"] = ocean.get(
            "ocean_condition",
            "Unknown",
        )

        if marine:
            obs = marine.get("observations", {})

            args["temperature"] = obs.get(
                "sea_surface_temperature"
            )

            args["chlorophyll"] = obs.get(
                "chlorophyll"
            )

    return args


# ============================================================
# STATE UPDATE
# ============================================================

def update_state(
    name: str,
    result: Dict[str, Any],
    state: Dict[str, Any],
) -> None:

    clean_result = safe_json_value(result)

    state["tool_history"].append(
        {
            "tool": name,
            "result": clean_result,
        }
    )

    mapping = {
        "get_marine_observations": "marine",
        "get_marine_weather": "weather",
        "run_fish_agent": "fish",
        "run_ocean_agent": "ocean",
        "run_ecosystem_agent": "ecosystem",
        "run_weather_agent": "weather_analysis",
        "run_evidence_agent": "evidence",
        "run_uncertainty_agent": "uncertainty",
        "run_causal_agent": "causal",
        "run_risk_agent": "risk",
        "run_reasoning_agent": "reasoning",
        "run_debate_agent": "debate",
        "run_alert_agent": "alerts",
        "run_route_agent": "route",
        "run_geofence_agent": "geofence",
    }

    state_name = mapping.get(name)

    if state_name:
        state[state_name] = clean_result


# ============================================================
# GEMINI FUNCTION RESULT
# ============================================================

def build_function_result(
    step: Any,
    result: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "type": "function_result",
        "name": getattr(step, "name", ""),
        "call_id": getattr(step, "id", None),
        "result": [
            {
                "type": "text",
                "text": json.dumps(
                    safe_json_value(result),
                    ensure_ascii=False,
                ),
            }
        ],
    }


# ============================================================
# DIRECT TOOL EXECUTION
#
# IMPORTANT:
# Mandatory fallback stages are executed by calling the actual
# ORCA agent function directly. This avoids the blocking path
# observed through execute_tool_call().
# ============================================================

def execute_direct_tool(
    tool_name: str,
    state: Dict[str, Any],
) -> Dict[str, Any]:

    context = state["context"]

    if tool_name == "get_marine_observations":
        return get_marine_observations(
            lat=context["latitude"],
            lon=context["longitude"],
            date=context["observation_date"],
        )

    if tool_name == "get_marine_weather":
        return get_marine_weather(
            lat=context["latitude"],
            lon=context["longitude"],
        )

    marine = state.get("marine") or {}
    observations = marine.get(
        "observations",
        {},
    )

    temperature = observations.get(
        "sea_surface_temperature"
    )

    chlorophyll = observations.get(
        "chlorophyll"
    )

    if tool_name == "run_fish_agent":
        return run_fish_agent(
            species=context["species"],
            temperature=temperature,
            chlorophyll=chlorophyll,
        )

    if tool_name == "run_ocean_agent":
        return run_ocean_agent(
            temperature=temperature,
            chlorophyll=chlorophyll,
            salinity=context["salinity"],
        )

    if tool_name == "run_evidence_agent":
        return run_evidence_agent(
            species=context["species"],
            temperature=temperature,
            chlorophyll=chlorophyll,
            salinity=context["salinity"],
        )

    if tool_name == "run_uncertainty_agent":
        return run_uncertainty_agent(
            temperature=temperature,
            chlorophyll=chlorophyll,
            salinity=context["salinity"],
        )

    if tool_name == "run_ecosystem_agent":
        fish = unwrap_result(
            state.get("fish") or {}
        )

        ocean = unwrap_result(
            state.get("ocean") or {}
        )

        return run_ecosystem_agent(
            fish_risk=fish.get(
                "risk",
                "Unknown",
            ),
            ocean_condition=ocean.get(
                "ocean_condition",
                "Unknown",
            ),
            temperature=temperature,
            chlorophyll=chlorophyll,
        )

    if tool_name == "run_risk_agent":
        fish = unwrap_result(
            state.get("fish") or {}
        )

        ocean = unwrap_result(
            state.get("ocean") or {}
        )

        ecosystem = unwrap_result(
            state.get("ecosystem") or {}
        )

        return run_risk_agent(
            fish_risk=fish.get(
                "risk",
                "Unknown",
            ),
            ocean_condition=ocean.get(
                "ocean_condition",
                "Unknown",
            ),
            ecosystem_status=ecosystem.get(
                "ecosystem_status",
                "Unknown",
            ),
        )

    if tool_name == "run_causal_agent":
        fish = unwrap_result(
            state.get("fish") or {}
        )

        ocean = unwrap_result(
            state.get("ocean") or {}
        )

        return run_causal_agent(
            temperature=temperature,
            chlorophyll=chlorophyll,
            salinity=context["salinity"],
            fish_risk=fish.get(
                "risk",
                "Unknown",
            ),
            ocean_condition=ocean.get(
                "ocean_condition",
                "Unknown",
            ),
        )

    if tool_name == "run_weather_agent":
        weather = state.get("weather") or {}
        weather_obs = weather.get(
            "observations",
            {},
        )

        return run_weather_agent(
            wind_speed=weather_obs.get(
                "wind_speed"
            ),
            wave_height=weather_obs.get(
                "wave_height"
            ),
            rainfall=weather_obs.get(
                "rainfall"
            ),
            weather_condition=weather_obs.get(
                "weather_condition",
                "Unknown",
            ),
        )

    if tool_name == "run_alert_agent":
        weather = state.get("weather") or {}
        weather_obs = weather.get(
            "observations",
            {},
        )

        return run_alert_agent(
            wind_speed=weather_obs.get(
                "wind_speed"
            ),
            wave_height=weather_obs.get(
                "wave_height"
            ),
            rainfall=weather_obs.get(
                "rainfall"
            ),
            weather_condition=weather_obs.get(
                "weather_condition",
                "Unknown",
            ),
        )

    return {
        "success": False,
        "error": (
            f"Direct execution is not implemented "
            f"for mandatory tool: {tool_name}"
        ),
    }


# ============================================================
# MANDATORY STAGES
# ============================================================

def get_mandatory_agents(
    query: str
) -> List[str]:

    routes = deterministic_routes(
        query
    )

    if "fish" in routes:
        return [
            "get_marine_observations",
            "run_fish_agent",
            "run_ocean_agent",
            "run_ecosystem_agent",
            "run_risk_agent",
            "run_evidence_agent",
            "run_uncertainty_agent",
            "run_causal_agent",
        ]

    if "ocean" in routes:
        return [
            "get_marine_observations",
            "run_ocean_agent",
            "run_ecosystem_agent",
            "run_risk_agent",
            "run_uncertainty_agent",
        ]

    if "route" in routes:
        return [
            "get_marine_weather",
            "run_weather_agent",
            "run_route_agent",
            "run_alert_agent",
        ]

    if "weather" in routes:
        return [
            "get_marine_weather",
            "run_weather_agent",
            "run_alert_agent",
        ]

    if "pfz" in routes:
        return [
            "get_marine_observations",
            "run_fish_agent",
            "run_ocean_agent",
            "run_evidence_agent",
            "run_uncertainty_agent",
        ]

    return [
        "get_marine_observations",
        "run_evidence_agent",
        "run_uncertainty_agent",
    ]


def ensure_mandatory_analysis(
    query: str,
    state: Dict[str, Any],
) -> None:

    mandatory = get_mandatory_agents(
        query
    )

    state_names = {
        "get_marine_observations": "marine",
        "get_marine_weather": "weather",
        "run_fish_agent": "fish",
        "run_ocean_agent": "ocean",
        "run_ecosystem_agent": "ecosystem",
        "run_risk_agent": "risk",
        "run_evidence_agent": "evidence",
        "run_uncertainty_agent": "uncertainty",
        "run_causal_agent": "causal",
        "run_weather_agent": "weather_analysis",
        "run_alert_agent": "alerts",
        "run_route_agent": "route",
    }

    print(
        "\nChecking mandatory ORCA stages..."
    )

    for tool_name in mandatory:

        state_name = state_names.get(
            tool_name
        )

        if not state_name:
            continue

        if state.get(
            state_name
        ) is not None:
            continue

        print(
            f"Mandatory stage missing: "
            f"{tool_name}"
        )

        if tool_name not in TOOL_FUNCTIONS:
            print(
                f"Tool unavailable: "
                f"{tool_name}"
            )
            continue

        print(
            f"FORCED DIRECT EXECUTION: "
            f"{tool_name}"
        )

        try:

            result = execute_direct_tool(
                tool_name,
                state,
            )

            update_state(
                tool_name,
                result,
                state,
            )

            print(
                f"Completed mandatory stage: "
                f"{tool_name}"
            )

        except Exception as exc:

            print(
                f"Mandatory stage error for "
                f"{tool_name}: {exc}"
            )

            result = {
                "success": False,
                "error": str(exc),
                "tool": tool_name,
            }

            update_state(
                tool_name,
                result,
                state,
            )


# ============================================================
# FINAL SYNTHESIS
# ============================================================

def build_final_synthesis_prompt(
    query: str,
    state: Dict[str, Any],
) -> str:

    useful_state = {
        "trusted_context":
            state.get("context"),

        "marine":
            state.get("marine"),

        "weather":
            state.get("weather"),

        "fish":
            state.get("fish"),

        "ocean":
            state.get("ocean"),

        "ecosystem":
            state.get("ecosystem"),

        "risk":
            state.get("risk"),

        "evidence":
            state.get("evidence"),

        "uncertainty":
            state.get("uncertainty"),

        "causal":
            state.get("causal"),

        "reasoning":
            state.get("reasoning"),

        "debate":
            state.get("debate"),

        "weather_analysis":
            state.get("weather_analysis"),

        "alerts":
            state.get("alerts"),
    }

    return f"""
You are ORCA's final scientific explanation layer.

USER QUESTION:
{query}

ORCA ANALYSIS STATE:
{json.dumps(
    safe_json_value(
        useful_state
    ),
    indent=2,
    ensure_ascii=False,
)}

Use ONLY the supplied ORCA information.

Rules:
- Do not invent measurements.
- Do not invent research.
- Do not invent weather.
- Do not invent fish abundance.
- Do not invent catch probability.
- Do not claim direct causation.
- Preserve the requested date.
- Preserve the requested location.
- Treat historical data as historical.
- Treat missing values as unavailable.
- Use actual Evidence Agent findings.
- Use actual Causal Agent findings.
- Use actual Risk Agent findings.
- Use actual Uncertainty Agent findings.
- Distinguish observations from interpretations.

Return ONLY JSON:

{{
  "answer": "clear scientific answer",
  "key_findings": [
    "finding 1",
    "finding 2"
  ],
  "recommendation": "decision-support recommendation",
  "uncertainty": "uncertainty statement",
  "sources_used": [
    "source 1",
    "source 2"
  ]
}}
"""


def final_synthesis(
    query: str,
    state: Dict[str, Any],
) -> Dict[str, Any]:

    print(
        "LLM final synthesis started..."
    )

    try:

        response = client.interactions.create(

            model=
                GEMINI_MODEL,

            input=
                build_final_synthesis_prompt(
                    query,
                    state,
                ),

            response_format={

                "type":
                    "text",

                "mime_type":
                    "application/json",
            },
        )

        parsed = parse_json_object(
            extract_response_text(
                response
            )
        )

        print(
            "LLM final synthesis received."
        )

        return {
            "llm_used": True,
            "model": GEMINI_MODEL,
            "answer": str(
                parsed.get(
                    "answer",
                    ""
                )
            ).strip(),
            "key_findings": parsed.get(
                "key_findings",
                []
            ),
            "recommendation": str(
                parsed.get(
                    "recommendation",
                    ""
                )
            ),
            "uncertainty": str(
                parsed.get(
                    "uncertainty",
                    ""
                )
            ),
            "sources_used": parsed.get(
                "sources_used",
                []
            ),
        }

    except Exception as exc:

        print(
            "LLM final synthesis error:",
            repr(exc)
        )

        return {
            "llm_used": False,
            "model": GEMINI_MODEL,
            "answer": "",
            "key_findings": [],
            "recommendation": "",
            "uncertainty":
                "Final LLM synthesis unavailable.",
            "sources_used": [],
            "error": str(exc),
        }


# ============================================================
# MAIN AGENTIC LOOP
# ============================================================

def run_agentic_llm(
    query: str,
    lat: float = 9.5,
    lon: float = 76.0,
    date: str = "2020-05-01",
    salinity: float = 34.0,
    species: str = "Indian Oil Sardine",
    max_tool_rounds: int = 8,
) -> Dict[str, Any]:

    print(
        "\n=================================================="
    )

    print(
        "ORCA LLM AGENTIC LOOP STARTED"
    )

    print(
        "=================================================="
    )

    context = build_trusted_context(
        query=query,
        lat=lat,
        lon=lon,
        date=date,
        salinity=salinity,
        species=species,
    )

    state = create_state(
        context
    )

    print(
        "\nTRUSTED CONTEXT:"
    )

    print(
        json.dumps(
            context,
            indent=2
        )
    )

    prompt = f"""
You are ORCA's LLM orchestration brain.

USER QUESTION:
{query}

TRUSTED CONTEXT:
{json.dumps(
    context,
    indent=2,
    ensure_ascii=False
)}

Available ORCA tools:
{json.dumps(
    list(TOOL_FUNCTIONS.keys()),
    indent=2
)}

ORCA controls:
- latitude
- longitude
- observation date
- salinity
- species

Never change those values.

For a fish productivity question, use the
marine observations, fish, ocean, ecosystem,
evidence, uncertainty, causal and risk stages.

Use actual tool results only.

When sufficient specialist results are available,
request the final answer.
"""

    try:

        interaction = client.interactions.create(

            model=
                GEMINI_MODEL,

            input=
                prompt,

            tools=
                GEMINI_ORCA_TOOLS,
        )

    except Exception as exc:

        return {
            "success": False,
            "llm_used": False,
            "model": GEMINI_MODEL,
            "answer": "",
            "error": str(exc),
            "rounds": 0,
            "tool_calls": [],
            "trusted_context": context,
        }

    round_number = 0

    while round_number < max_tool_rounds:

        round_number += 1

        print(
            f"\nLLM tool round {round_number}"
        )

        steps = getattr(
            interaction,
            "steps",
            []
        )

        function_calls = [
            step
            for step in steps
            if getattr(
                step,
                "type",
                ""
            ) == "function_call"
        ]

        # ====================================================
        # GEMINI FINISHED
        # ====================================================

        if not function_calls:

            print(
                "\nGemini requested final answer."
            )

            # IMPORTANT:
            # The mandatory ORCA stages are now executed
            # directly, including Risk Agent.
            ensure_mandatory_analysis(
                query,
                state,
            )

            synthesis = final_synthesis(
                query,
                state,
            )

            state_summary = {
                "marine":
                    state["marine"] is not None,

                "weather":
                    state["weather"] is not None,

                "fish":
                    state["fish"] is not None,

                "ocean":
                    state["ocean"] is not None,

                "ecosystem":
                    state["ecosystem"] is not None,

                "risk":
                    state["risk"] is not None,

                "evidence":
                    state["evidence"] is not None,

                "uncertainty":
                    state["uncertainty"] is not None,

                "causal":
                    state["causal"] is not None,

                "reasoning":
                    state["reasoning"] is not None,

                "debate":
                    state["debate"] is not None,

                "alerts":
                    state["alerts"] is not None,
            }

            return {
                "success": True,
                "llm_used":
                    synthesis.get(
                        "llm_used",
                        False
                    ),
                "model":
                    GEMINI_MODEL,
                "answer":
                    synthesis.get(
                        "answer",
                        ""
                    ),
                "key_findings":
                    synthesis.get(
                        "key_findings",
                        []
                    ),
                "recommendation":
                    synthesis.get(
                        "recommendation",
                        ""
                    ),
                "uncertainty":
                    synthesis.get(
                        "uncertainty",
                        ""
                    ),
                "sources_used":
                    synthesis.get(
                        "sources_used",
                        []
                    ),
                "rounds":
                    round_number,
                "tool_calls":
                    state["tool_history"],
                "trusted_context":
                    context,
                "state_summary":
                    state_summary,
                "interaction_id":
                    getattr(
                        interaction,
                        "id",
                        None
                    ),
            }

        function_results = []

        # ====================================================
        # EXECUTE GEMINI REQUESTED TOOLS
        # ====================================================

        for step in function_calls:

            tool_name = getattr(
                step,
                "name",
                ""
            )

            raw_arguments = getattr(
                step,
                "arguments",
                {}
            )

            if isinstance(
                raw_arguments,
                str
            ):

                try:

                    raw_arguments = json.loads(
                        raw_arguments
                    )

                except Exception:

                    raw_arguments = {}

            print(
                f"Gemini requested: "
                f"{tool_name}"
            )

            print(
                f"Requested arguments: "
                f"{raw_arguments}"
            )

            safe_arguments = enforce_state(
                name=
                    tool_name,
                arguments=
                    raw_arguments,
                state=
                    state,
            )

            print(
                f"Executed arguments: "
                f"{safe_arguments}"
            )

            if tool_name in TOOL_FUNCTIONS:

                try:

                    result = execute_tool_call(

                        name=
                            tool_name,

                        arguments=
                            safe_arguments,
                    )

                except Exception as exc:

                    result = {
                        "success": False,
                        "error": str(exc),
                        "tool": tool_name,
                    }

            else:

                result = {
                    "success": False,
                    "error":
                        f"Unknown ORCA tool: "
                        f"{tool_name}",
                }

            update_state(
                name=
                    tool_name,
                result=
                    result,
                state=
                    state,
            )

            function_results.append(
                build_function_result(
                    step,
                    result,
                )
            )

        # ====================================================
        # SEND RESULTS BACK TO GEMINI
        # ====================================================

        try:

            interaction = client.interactions.create(

                model=
                    GEMINI_MODEL,

                previous_interaction_id=
                    interaction.id,

                input=
                    function_results,

                tools=
                    GEMINI_ORCA_TOOLS,
            )

        except Exception as exc:

            return {
                "success": False,
                "llm_used": True,
                "model": GEMINI_MODEL,
                "answer": "",
                "error": str(exc),
                "rounds": round_number,
                "tool_calls":
                    state["tool_history"],
                "trusted_context":
                    context,
            }

    # ========================================================
    # MAX ROUND FALLBACK
    # ========================================================

    print(
        "\nMaximum LLM tool rounds reached."
    )

    ensure_mandatory_analysis(
        query,
        state,
    )

    synthesis = final_synthesis(
        query,
        state,
    )

    return {
        "success": True,
        "llm_used":
            synthesis.get(
                "llm_used",
                False
            ),
        "model":
            GEMINI_MODEL,
        "answer":
            synthesis.get(
                "answer",
                ""
            ),
        "key_findings":
            synthesis.get(
                "key_findings",
                []
            ),
        "recommendation":
            synthesis.get(
                "recommendation",
                ""
            ),
        "uncertainty":
            synthesis.get(
                "uncertainty",
                ""
            ),
        "sources_used":
            synthesis.get(
                "sources_used",
                []
            ),
        "rounds":
            round_number,
        "tool_calls":
            state["tool_history"],
        "trusted_context":
            context,
        "max_rounds_reached":
            True,
    }


# ============================================================
# LEGACY SYNTHESIS
# ============================================================

def build_synthesis_prompt(
    query: str,
    plan: Dict[str, Any],
    observations: Dict[str, Any],
    agent_results: Dict[str, Any],
) -> str:

    return f"""
You are ORCA's scientific marine decision-support assistant.

USER QUESTION:
{query}

PLAN:
{json.dumps(
    plan,
    indent=2,
    ensure_ascii=False
)}

OBSERVATIONS:
{json.dumps(
    observations,
    indent=2,
    ensure_ascii=False
)}

SPECIALIST RESULTS:
{json.dumps(
    agent_results,
    indent=2,
    ensure_ascii=False
)}

Use ONLY the supplied information.

Do not invent:
- measurements
- research
- weather
- advisories
- fish abundance
- catch probability
- unsupported causation

Return ONLY JSON:

{{
  "answer": "clear answer",
  "key_findings": [],
  "recommendation": "decision-support recommendation",
  "uncertainty": "uncertainty statement",
  "sources_used": []
}}
"""


def synthesize_with_llm(
    query: str,
    plan: Dict[str, Any],
    observations: Dict[str, Any],
    agent_results: Dict[str, Any],
) -> Dict[str, Any]:

    print(
        "LLM synthesis started..."
    )

    try:

        response = client.interactions.create(

            model=
                GEMINI_MODEL,

            input=
                build_synthesis_prompt(
                    query,
                    plan,
                    observations,
                    agent_results,
                ),

            response_format={
                "type": "text",
                "mime_type": "application/json",
            },
        )

        parsed = parse_json_object(
            extract_response_text(
                response
            )
        )

        return {
            "llm_used": True,
            "model": GEMINI_MODEL,
            "answer": str(
                parsed.get(
                    "answer",
                    ""
                )
            ),
            "key_findings": parsed.get(
                "key_findings",
                []
            ),
            "recommendation": str(
                parsed.get(
                    "recommendation",
                    ""
                )
            ),
            "uncertainty": str(
                parsed.get(
                    "uncertainty",
                    ""
                )
            ),
            "sources_used": parsed.get(
                "sources_used",
                []
            ),
        }

    except Exception as exc:

        return {
            "llm_used": False,
            "model": GEMINI_MODEL,
            "answer": "",
            "key_findings": [],
            "recommendation": "",
            "uncertainty":
                "LLM synthesis unavailable.",
            "sources_used": [],
            "error": str(exc),
        }


# ============================================================
# COMPATIBILITY ORCHESTRATION
# ============================================================

def orchestrate_with_llm(
    query: str,
    observations: Dict[str, Any] | None = None,
    agent_results: Dict[str, Any] | None = None,
    lat: float = 9.5,
    lon: float = 76.0,
    date: str = "2020-05-01",
    salinity: float = 34.0,
    species: str = "Indian Oil Sardine",
) -> Dict[str, Any]:

    plan = plan_with_llm(
        query
    )

    execution = run_agentic_llm(
        query=query,
        lat=lat,
        lon=lon,
        date=date,
        salinity=salinity,
        species=species,
    )

    return {
        "llm_orchestration": {
            "enabled": True,
            "model": GEMINI_MODEL,
            "planning_used":
                plan.get(
                    "llm_used",
                    False
                ),
            "agentic_loop_used":
                execution.get(
                    "llm_used",
                    False
                ),
        },
        "llm_plan": plan,
        "agentic_execution": execution,
    }


# ============================================================
# STATUS
# ============================================================

def get_orchestrator_status() -> Dict[str, Any]:

    return {
        "enabled": True,
        "model": GEMINI_MODEL,
        "api_key_loaded":
            bool(GEMINI_API_KEY),
        "tool_count":
            len(TOOL_FUNCTIONS),
        "tools":
            list(
                TOOL_FUNCTIONS.keys()
            ),
    }

# ============================================================
# END
# ============================================================

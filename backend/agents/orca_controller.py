# ============================================================
# ORCA - Marine Ecosystem Intelligence System
# Main Agent Controller
#
# LLM-ORCHESTRATED VERSION
#
# Architecture:
#
# User Query
#     ↓
# Gemini LLM Orchestrator
#     ↓
# Query Planning / Agent Selection
#     ↓
# ORCA Specialist Agents
#     ↓
# Evidence / Reasoning / Risk / Uncertainty
#     ↓
# Gemini LLM Synthesis
#     ↓
# Final ORCA Response
# ============================================================

from datetime import datetime
from typing import Any, Dict, List, Optional


# ------------------------------------------------------------
# Marine data
# ------------------------------------------------------------

from data.marine_data import (
    get_marine_data,
    extract_marine_values,
    get_spatial_marine_data,
)


# ------------------------------------------------------------
# Query planning / routing
# ------------------------------------------------------------

from agents.planner_agent import (
    plan_query,
    build_execution_plan,
)

from agents.query_router import (
    route_query,
)


# ------------------------------------------------------------
# LLM ORCHESTRATOR
# ------------------------------------------------------------

from agents.llm_orchestrator import (
    plan_with_llm,
    synthesize_with_llm,
)


# ------------------------------------------------------------
# Specialist agents
# ------------------------------------------------------------

from agents.fish_agent import (
    analyze_fish,
)

from agents.ocean_agent import (
    analyze_ocean,
)

from agents.ecosystem_agent import (
    analyze_ecosystem,
)

from agents.risk_agent import (
    calculate_risk,
)

from agents.uncertainty_agent import (
    calculate_uncertainty,
)

from agents.evidence_agent import (
    find_evidence,
)

from agents.reasoning_agent import (
    generate_reasoning,
)

from agents.debate_agent import (
    analyze_agent_disagreement,
)

from agents.causal_reasoning_agent import (
    build_causal_chain,
)


# ------------------------------------------------------------
# Decision / visualization / reporting
# ------------------------------------------------------------

from agents.decision_agent import (
    generate_decision,
)

from agents.visualization_agent import (
    create_visualization_data,
)

from agents.report_agent import (
    generate_report,
)


# ------------------------------------------------------------
# Weather / safety
# ------------------------------------------------------------

from data.weather_data import (
    get_weather_data,
)

from agents.weather_agent import (
    analyze_weather,
)

from agents.alert_agent import (
    generate_alerts,
)


# ------------------------------------------------------------
# Route / geofence / PFZ
# ------------------------------------------------------------

from agents.route_agent import (
    analyze_route,
)

from agents.geofence_agent import (
    analyze_geofence,
)

from agents.pfz_spatial_agent import (
    analyze_spatial_pfz,
)


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

DEFAULT_SPECIES = "Indian Oil Sardine"


# ============================================================
# SAFE HELPERS
# ============================================================

def safe_dict(value: Any) -> Dict[str, Any]:
    """
    Return a dictionary when possible.
    """

    if isinstance(value, dict):
        return value

    return {}


def safe_list(value: Any) -> List[Any]:
    """
    Return a list when possible.
    """

    if isinstance(value, list):
        return value

    return []


# ============================================================
# WEATHER CODE CONVERSION
# ============================================================

def weather_code_to_condition(weather_code):
    """
    Convert Open-Meteo WMO weather codes into
    human-readable weather conditions.
    """

    if weather_code is None:
        return "Unknown"

    if weather_code == 0:
        return "Clear"

    if weather_code in [1, 2, 3]:
        return "Cloudy"

    if weather_code in [45, 48]:
        return "Fog"

    if weather_code in [51, 53, 55, 56, 57]:
        return "Drizzle"

    if weather_code in [61, 63, 65, 66, 67]:
        return "Rain"

    if weather_code in [71, 73, 75, 77]:
        return "Snow"

    if weather_code in [80, 81, 82]:
        return "Rain Showers"

    if weather_code == 95:
        return "Thunderstorm"

    if weather_code in [96, 99]:
        return "Thunderstorm with Hail"

    return "Unknown"


# ============================================================
# LLM AGENT PLAN NORMALIZATION
# ============================================================

def normalize_llm_plan(
    query: str,
    llm_plan: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Normalize and validate the plan returned by Gemini.

    The LLM may return only a subset of agents. ORCA then
    adds necessary dependency agents so the scientific
    pipeline remains coherent.
    """

    plan = safe_dict(
        llm_plan
    )

    selected = plan.get(
        "selected_agents",
        []
    )

    if not isinstance(
        selected,
        list
    ):
        selected = []

    selected = [
        str(agent).strip().lower()
        for agent in selected
        if str(agent).strip()
    ]

    # --------------------------------------------------------
    # Remove unknown agent names
    # --------------------------------------------------------

    allowed_agents = {
        "fish",
        "ocean",
        "ecosystem",
        "weather",
        "risk",
        "evidence",
        "reasoning",
        "uncertainty",
        "debate",
        "causal",
        "alerts",
        "route",
        "geofence",
        "pfz",
    }

    selected = [
        agent
        for agent in selected
        if agent in allowed_agents
    ]

    # --------------------------------------------------------
    # Keyword fallback
    # --------------------------------------------------------

    query_lower = query.lower()

    # Fish-related questions
    fish_keywords = [
        "fish",
        "sardine",
        "fishing",
        "fishery",
        "productivity",
        "catch",
        "species",
        "stock",
        "biomass",
    ]

    # Ocean-related questions
    ocean_keywords = [
        "ocean",
        "sea",
        "sst",
        "temperature",
        "chlorophyll",
        "salinity",
        "marine ecosystem",
        "marine condition",
    ]

    # Weather-related questions
    weather_keywords = [
        "weather",
        "wind",
        "rain",
        "rainfall",
        "wave",
        "waves",
        "storm",
        "forecast",
        "tomorrow",
        "today",
    ]

    # Route-related questions
    route_keywords = [
        "route",
        "navigation",
        "travel",
        "journey",
        "go fishing",
        "safe to go",
        "safe route",
    ]

    # PFZ-related questions
    pfz_keywords = [
        "pfz",
        "potential fishing zone",
        "fishing zone",
        "fishing area",
        "hotspot",
        "best fishing area",
    ]

    # Evidence-related questions
    evidence_keywords = [
        "research",
        "paper",
        "evidence",
        "study",
        "scientific",
        "literature",
        "publication",
    ]

    # Causal questions
    causal_keywords = [
        "why",
        "cause",
        "caused",
        "because",
        "reason",
        "impact",
        "effect",
        "influence",
    ]

    if any(
        word in query_lower
        for word in fish_keywords
    ):
        selected.append("fish")

    if any(
        word in query_lower
        for word in ocean_keywords
    ):
        selected.append("ocean")

    if any(
        word in query_lower
        for word in weather_keywords
    ):
        selected.append("weather")

    if any(
        word in query_lower
        for word in route_keywords
    ):
        selected.append("route")

    if any(
        word in query_lower
        for word in pfz_keywords
    ):
        selected.append("pfz")

    if any(
        word in query_lower
        for word in evidence_keywords
    ):
        selected.append("evidence")

    if any(
        word in query_lower
        for word in causal_keywords
    ):
        selected.append("causal")

    # --------------------------------------------------------
    # Core ORCA dependencies
    # --------------------------------------------------------

    if "fish" in selected:
        selected.extend([
            "ocean",
            "ecosystem",
            "risk",
            "evidence",
            "reasoning",
            "uncertainty",
            "debate",
        ])

    if "ocean" in selected:
        selected.extend([
            "ecosystem",
            "risk",
            "uncertainty",
        ])

    if "weather" in selected:
        selected.extend([
            "risk",
            "alerts",
        ])

    if "route" in selected:
        selected.extend([
            "weather",
            "risk",
            "alerts",
        ])

    if "pfz" in selected:
        selected.extend([
            "fish",
            "ocean",
            "evidence",
            "uncertainty",
        ])

    if "geofence" in selected:
        selected.append(
            "alerts"
        )

    if "causal" in selected:
        selected.extend([
            "reasoning",
            "evidence",
            "uncertainty",
        ])

    # --------------------------------------------------------
    # General fallback
    # --------------------------------------------------------

    if not selected:
        selected = [
            "fish",
            "ocean",
            "evidence",
            "reasoning",
            "uncertainty",
        ]

    # --------------------------------------------------------
    # Deduplicate while preserving order
    # --------------------------------------------------------

    selected_unique = []

    for agent in selected:

        if agent not in selected_unique:
            selected_unique.append(
                agent
            )

    normalized = {
        "intent": plan.get(
            "intent",
            "Marine ecosystem analysis"
        ),

        "complexity": plan.get(
            "complexity",
            "moderate"
        ),

        "selected_agents": selected_unique,

        "reason": plan.get(
            "reason",
            "ORCA selected specialist agents for the request."
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
                "weather" in selected_unique
                or "route" in selected_unique
            )
        ),

        "requires_research_evidence": bool(
            plan.get(
                "requires_research_evidence",
                "evidence" in selected_unique
            )
        ),

        "llm_planning_failed": bool(
            plan.get(
                "llm_planning_failed",
                False
            )
        ),
    }

    return normalized


# ============================================================
# BASIC ORCA ANALYSIS
# ============================================================

def run_orca(
    species,
    temperature,
    chlorophyll,
    salinity=34
):
    """
    Run the core ORCA environmental assessment.
    """

    # --------------------------------------------------------
    # Fish agent
    # --------------------------------------------------------

    fish_result = analyze_fish(
        species,
        temperature,
        chlorophyll
    )

    # --------------------------------------------------------
    # Ocean agent
    # --------------------------------------------------------

    ocean_result = analyze_ocean(
        temperature,
        chlorophyll,
        salinity
    )

    # --------------------------------------------------------
    # Ecosystem agent
    # --------------------------------------------------------

    ecosystem_result = analyze_ecosystem(
        fish_result["risk"],
        ocean_result["ocean_condition"],
        temperature,
        chlorophyll
    )

    # --------------------------------------------------------
    # Risk agent
    # --------------------------------------------------------

    risk_result = calculate_risk(
        fish_result["risk"],
        ocean_result["ocean_condition"],
        ecosystem_result["ecosystem_status"]
    )

    # --------------------------------------------------------
    # Uncertainty agent
    # --------------------------------------------------------

    uncertainty_result = calculate_uncertainty(
        temperature,
        chlorophyll,
        salinity
    )

    # --------------------------------------------------------
    # Evidence agent
    # --------------------------------------------------------

    evidence_result = find_evidence(
        species,
        temperature,
        chlorophyll,
        salinity
    )

    # --------------------------------------------------------
    # Reasoning agent
    # --------------------------------------------------------

    reasoning_result = generate_reasoning(
        species,
        temperature,
        chlorophyll,
        salinity,
        fish_result,
        ocean_result,
        ecosystem_result,
        risk_result
    )

    # --------------------------------------------------------
    # Debate agent
    # --------------------------------------------------------

    debate_result = analyze_agent_disagreement(
        fish_result=fish_result,
        ocean_result=ocean_result,
        ecosystem_result=ecosystem_result,
        reasoning_result=reasoning_result,
        evidence_result=evidence_result
    )

    # --------------------------------------------------------
    # Causal reasoning
    # --------------------------------------------------------

    causal_result = build_causal_chain(
        temperature=temperature,
        chlorophyll=chlorophyll,
        salinity=salinity,
        fish_risk=fish_result["risk"],
        ocean_condition=ocean_result["ocean_condition"]
    )

    # --------------------------------------------------------
    # Decision support
    # --------------------------------------------------------

    decision_result = generate_decision(
        query="Marine ecosystem assessment",
        risk_analysis=risk_result,
        uncertainty_analysis=uncertainty_result,
        evidence=evidence_result,
        debate=debate_result
    )

    # --------------------------------------------------------
    # Observations
    # --------------------------------------------------------

    observations = {
        "sea_surface_temperature": temperature,
        "chlorophyll": chlorophyll,
        "salinity": salinity
    }

    # --------------------------------------------------------
    # Visualization
    # --------------------------------------------------------

    visualization_result = create_visualization_data(
        observations=observations,
        analysis=risk_result
    )

    # --------------------------------------------------------
    # Alerts
    # --------------------------------------------------------

    alerts_result = generate_alerts(
        wind_speed=None,
        wave_height=None,
        rainfall=None,
        weather_condition="Unknown"
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    report_result = generate_report(
        query="Marine ecosystem assessment",
        species=species,
        observations=observations,
        fish_analysis=fish_result,
        ocean_analysis=ocean_result,
        ecosystem_analysis=ecosystem_result,
        risk_analysis=risk_result,
        uncertainty_analysis=uncertainty_result,
        evidence=evidence_result,
        debate=debate_result,
        alerts=alerts_result
    )

    return {
        "project": "ORCA",
        "timestamp": datetime.utcnow().isoformat(),
        "species": species,
        "observations": observations,

        "fish_analysis": fish_result,
        "ocean_analysis": ocean_result,
        "ecosystem_analysis": ecosystem_result,

        "risk_analysis": risk_result,
        "uncertainty_analysis": uncertainty_result,

        "evidence": evidence_result,
        "agent_debate": debate_result,

        "reasoning": reasoning_result,
        "causal_reasoning": causal_result,

        "decision": decision_result,
        "alerts": alerts_result,

        "visualization": visualization_result,
        "report": report_result,

        "system_status": "ORCA analysis completed"
    }


# ============================================================
# ORCA ANALYSIS WITH LOCATION
# ============================================================

def run_orca_with_location(
    species,
    lat,
    lon,
    date,
    salinity=34
):
    """
    Run ORCA using marine observations for a
    specific location and date.
    """

    marine_data = get_marine_data(
        lat,
        lon,
        date
    )

    temperature, chlorophyll = extract_marine_values(
        marine_data
    )

    result = run_orca(
        species=species,
        temperature=temperature,
        chlorophyll=chlorophyll,
        salinity=salinity
    )

    result["location"] = {
        "latitude": lat,
        "longitude": lon
    }

    result["date"] = date

    result["data_sources"] = {
        "sst": "NOAA CoastWatch MUR SST",
        "chlorophyll": "INCOIS Oceansat-2 OCM"
    }

    result["raw_marine_data"] = marine_data

    result["historical_data_note"] = (
        "The requested date determines whether "
        "the returned observation is historical or recent. "
        "ORCA does not label historical observations as current."
    )

    return result


# ============================================================
# FULL LLM-ORCHESTRATED ORCA PIPELINE
# ============================================================

def run_agentic_orca(
    query,
    species=DEFAULT_SPECIES,
    lat=9.5,
    lon=76.0,
    date=None,
    salinity=34
):
    """
    Full ORCA LLM-orchestrated multi-agent pipeline.

    Architecture:

    Query
       ↓
    Gemini LLM
       ↓
    LLM Planning
       ↓
    Existing ORCA Planner + Router
       ↓
    Marine Data
       ↓
    Specialist Agents
       ↓
    Evidence / Reasoning / Risk / Uncertainty
       ↓
    Gemini LLM Synthesis
       ↓
    Final Answer
    """

    # ========================================================
    # 1. DATE
    # ========================================================

    if date is None:
        date = "2020-05-01"

    # ========================================================
    # 2. LLM PLANNING
    # ========================================================

    llm_plan_raw = plan_with_llm(
        query
    )

    llm_plan = normalize_llm_plan(
        query,
        llm_plan_raw
    )

    # ========================================================
    # 3. EXISTING ORCA PLANNER
    # ========================================================

    planner_result = plan_query(
        query
    )

    # ========================================================
    # 4. EXISTING QUERY ROUTER
    # ========================================================

    router_result = route_query(
        query
    )

    router_result = safe_dict(
        router_result
    )

    # ========================================================
    # 5. EXISTING EXECUTION PLAN
    # ========================================================

    execution_plan = build_execution_plan(
        query
    )

    # ========================================================
    # 6. MERGE LLM + RULE-BASED ROUTING
    # ========================================================

    selected_agents = set(
        llm_plan.get(
            "selected_agents",
            []
        )
    )

    routes = safe_list(
        router_result.get(
            "routes",
            []
        )
    )

    for route in routes:

        route_name = str(
            route
        ).lower()

        if route_name == "weather":
            selected_agents.add(
                "weather"
            )

        if route_name == "route":
            selected_agents.add(
                "route"
            )

        if route_name == "pfz":
            selected_agents.add(
                "pfz"
            )

        if route_name == "geofence":
            selected_agents.add(
                "geofence"
            )

        if route_name == "general":
            selected_agents.update([
                "fish",
                "ocean",
                "evidence",
                "reasoning",
                "uncertainty"
            ])

    # ========================================================
    # 7. MARINE DATA
    # ========================================================

    marine_data = get_marine_data(
        lat,
        lon,
        date
    )

    temperature, chlorophyll = extract_marine_values(
        marine_data
    )

    # ========================================================
    # 8. AGENT RESULT CONTAINER
    # ========================================================

    agent_results: Dict[str, Any] = {}

    # ========================================================
    # 9. FISH AGENT
    # ========================================================

    if (
        "fish" in selected_agents
        or "pfz" in selected_agents
        or "ecosystem" in selected_agents
    ):

        fish_result = analyze_fish(
            species,
            temperature,
            chlorophyll
        )

        agent_results["fish"] = fish_result

    else:

        fish_result = {
            "species": species,
            "risk": "Not evaluated",
            "data_available": False
        }

    # ========================================================
    # 10. OCEAN AGENT
    # ========================================================

    if (
        "ocean" in selected_agents
        or "fish" in selected_agents
        or "ecosystem" in selected_agents
        or "pfz" in selected_agents
    ):

        ocean_result = analyze_ocean(
            temperature,
            chlorophyll,
            salinity
        )

        agent_results["ocean"] = ocean_result

    else:

        ocean_result = {
            "ocean_condition": "Not evaluated",
            "data_available": False
        }

    # ========================================================
    # 11. ECOSYSTEM AGENT
    # ========================================================

    if (
        "ecosystem" in selected_agents
        or "fish" in selected_agents
        or "ocean" in selected_agents
    ):

        ecosystem_result = analyze_ecosystem(
            fish_result.get(
                "risk",
                "Unknown"
            ),

            ocean_result.get(
                "ocean_condition",
                "Unknown"
            ),

            temperature,
            chlorophyll
        )

        agent_results[
            "ecosystem"
        ] = ecosystem_result

    else:

        ecosystem_result = {
            "ecosystem_status": "Not evaluated"
        }

    # ========================================================
    # 12. RISK AGENT
    # ========================================================

    if (
        "risk" in selected_agents
        or "fish" in selected_agents
        or "ocean" in selected_agents
        or "ecosystem" in selected_agents
        or "weather" in selected_agents
        or "route" in selected_agents
    ):

        risk_result = calculate_risk(
            fish_result.get(
                "risk",
                "Unknown"
            ),

            ocean_result.get(
                "ocean_condition",
                "Unknown"
            ),

            ecosystem_result.get(
                "ecosystem_status",
                "Unknown"
            )
        )

        agent_results[
            "risk"
        ] = risk_result

    else:

        risk_result = {
            "overall_risk": "Not evaluated"
        }

    # ========================================================
    # 13. UNCERTAINTY AGENT
    # ========================================================

    if (
        "uncertainty" in selected_agents
        or "risk" in selected_agents
        or "reasoning" in selected_agents
        or "evidence" in selected_agents
    ):

        uncertainty_result = calculate_uncertainty(
            temperature,
            chlorophyll,
            salinity
        )

        agent_results[
            "uncertainty"
        ] = uncertainty_result

    else:

        uncertainty_result = {
            "confidence": None,
            "uncertainty_level": "Not evaluated"
        }

    # ========================================================
    # 14. EVIDENCE AGENT
    # ========================================================

    if (
        "evidence" in selected_agents
        or "fish" in selected_agents
        or "reasoning" in selected_agents
        or "causal" in selected_agents
        or "pfz" in selected_agents
    ):

        evidence_result = find_evidence(
            species,
            temperature,
            chlorophyll,
            salinity
        )

        agent_results[
            "evidence"
        ] = evidence_result

    else:

        evidence_result = {
            "species": species,
            "evidence": [],
            "evidence_count": 0,
            "evidence_available": False
        }

    # ========================================================
    # 15. REASONING AGENT
    # ========================================================

    if (
        "reasoning" in selected_agents
        or "fish" in selected_agents
        or "evidence" in selected_agents
        or "causal" in selected_agents
    ):

        reasoning_result = generate_reasoning(
            species,
            temperature,
            chlorophyll,
            salinity,
            fish_result,
            ocean_result,
            ecosystem_result,
            risk_result
        )

        agent_results[
            "reasoning"
        ] = reasoning_result

    else:

        reasoning_result = {
            "species": species,
            "overall_risk": risk_result.get(
                "overall_risk",
                "Unknown"
            ),
            "reasoning": [],
            "causal_chain": []
        }

    # ========================================================
    # 16. DEBATE AGENT
    # ========================================================

    if (
        "debate" in selected_agents
        or "fish" in selected_agents
        or "ocean" in selected_agents
        or "ecosystem" in selected_agents
    ):

        debate_result = analyze_agent_disagreement(
            fish_result=fish_result,
            ocean_result=ocean_result,
            ecosystem_result=ecosystem_result,
            reasoning_result=reasoning_result,
            evidence_result=evidence_result
        )

        agent_results[
            "debate"
        ] = debate_result

    else:

        debate_result = {
            "disagreement_detected": False,
            "explanation": "Debate not required for this query."
        }

    # ========================================================
    # 17. CAUSAL REASONING
    # ========================================================

    if (
        "causal" in selected_agents
        or "reasoning" in selected_agents
        or "fish" in selected_agents
    ):

        causal_result = build_causal_chain(
            temperature=temperature,
            chlorophyll=chlorophyll,
            salinity=salinity,

            fish_risk=fish_result.get(
                "risk",
                "Unknown"
            ),

            ocean_condition=ocean_result.get(
                "ocean_condition",
                "Unknown"
            )
        )

        agent_results[
            "causal"
        ] = causal_result

    else:

        causal_result = {
            "causal_chain": [],
            "evidence_links": [],
            "alternative_explanations": []
        }

    # ========================================================
    # 18. WEATHER AGENT
    # ========================================================

    weather_data = None
    weather_result = None

    needs_weather = (
        "weather" in selected_agents
        or "route" in selected_agents
        or "alerts" in selected_agents
    )

    if needs_weather:

        weather_data = get_weather_data(
            lat,
            lon
        )

        weather_code = weather_data.get(
            "weather_code"
        )

        weather_condition = weather_code_to_condition(
            weather_code
        )

        weather_result = analyze_weather(
            weather_data.get(
                "wind_speed"
            ) or 0,

            weather_data.get(
                "wave_height"
            ) or 0,

            weather_data.get(
                "rainfall"
            ) or 0,

            weather_condition
        )

        agent_results[
            "weather"
        ] = weather_result

    # ========================================================
    # 19. WEATHER ALERTS
    # ========================================================

    if (
        "alerts" in selected_agents
        or needs_weather
    ):

        alerts_result = generate_alerts(

            wind_speed=(
                weather_data.get(
                    "wind_speed"
                )
                if weather_data
                else None
            ),

            wave_height=(
                weather_data.get(
                    "wave_height"
                )
                if weather_data
                else None
            ),

            rainfall=(
                weather_data.get(
                    "rainfall"
                )
                if weather_data
                else None
            ),

            weather_condition=(
                weather_result.get(
                    "weather_condition",
                    "Unknown"
                )
                if weather_result
                else "Unknown"
            )
        )

        agent_results[
            "alerts"
        ] = alerts_result

    else:

        alerts_result = {
            "overall_level": "Low",
            "alert_count": 0,
            "alerts": []
        }

    # ========================================================
    # 20. PFZ AGENT
    # ========================================================

    pfz_result = None

    if "pfz" in selected_agents:

        try:

            pfz_marine_data = get_spatial_marine_data(
                min_lat=lat - 0.4,
                max_lat=lat + 0.4,
                min_lon=lon - 0.4,
                max_lon=lon + 0.4,
                date=date,
                step=0.2
            )

            pfz_result = analyze_spatial_pfz(
                pfz_marine_data
            )

            agent_results[
                "pfz"
            ] = pfz_result

        except Exception as exc:

            pfz_result = {
                "status": "PFZ analysis failed",
                "error": str(exc)
            }

            agent_results[
                "pfz"
            ] = pfz_result

    # ========================================================
    # 21. GEOFENCE
    # ========================================================

    geofence_result = None

    if "geofence" in selected_agents:

        geofence_result = {
            "status": (
                "Geofence tool selected by "
                "LLM but requires route geometry input."
            )
        }

        agent_results[
            "geofence"
        ] = geofence_result

    # ========================================================
    # 22. ROUTE
    # ========================================================

    route_result = None

    if "route" in selected_agents:

        route_result = {
            "status": (
                "Route agent selected by "
                "LLM orchestration. Use the dedicated "
                "/route-analysis endpoint for full route geometry."
            )
        }

        agent_results[
            "route"
        ] = route_result

    # ========================================================
    # 23. OBSERVATIONS
    # ========================================================

    observations = {
        "sea_surface_temperature": temperature,
        "chlorophyll": chlorophyll,
        "salinity": salinity
    }

    if weather_data:

        observations.update({

            "wind_speed":
                weather_data.get(
                    "wind_speed"
                ),

            "wave_height":
                weather_data.get(
                    "wave_height"
                ),

            "rainfall":
                weather_data.get(
                    "rainfall"
                ),

        })

    # ========================================================
    # 24. DECISION
    # ========================================================

    decision_result = generate_decision(
        query=query,
        risk_analysis=risk_result,
        uncertainty_analysis=uncertainty_result,
        evidence=evidence_result,
        debate=debate_result,
        alerts=alerts_result
    )

    agent_results[
        "decision"
    ] = decision_result

    # ========================================================
    # 25. VISUALIZATION
    # ========================================================

    visualization_result = create_visualization_data(
        observations=observations,
        analysis=risk_result
    )

    agent_results[
        "visualization"
    ] = visualization_result

    # ========================================================
    # 26. REPORT
    # ========================================================

    report_result = generate_report(
        query=query,
        species=species,
        observations=observations,

        fish_analysis=fish_result,
        ocean_analysis=ocean_result,
        ecosystem_analysis=ecosystem_result,

        risk_analysis=risk_result,
        uncertainty_analysis=uncertainty_result,

        evidence=evidence_result,
        debate=debate_result,

        weather_analysis=weather_result,
        alerts=alerts_result
    )

    agent_results[
        "report"
    ] = report_result

    # ========================================================
    # 27. LLM FINAL SYNTHESIS
    # ========================================================

    llm_synthesis = synthesize_with_llm(
        query=query,

        plan=llm_plan,

        observations=observations,

        agent_results=agent_results
    )

    # ========================================================
    # 28. FINAL RESULT
    # ========================================================

    return {

        "project": "ORCA",

        "query": query,

        "timestamp":
            datetime.utcnow().isoformat(),

        "location": {
            "latitude": lat,
            "longitude": lon
        },

        "date": date,

        # ----------------------------------------------------
        # LLM ORCHESTRATION
        # ----------------------------------------------------

        "llm_orchestration": {

            "enabled": True,

            "planner": "Gemini",

            "model": llm_synthesis.get(
                "model"
            ) or llm_plan.get(
                "model",
                "gemini-3.5-flash"
            ),

            "selected_agents":
                llm_plan.get(
                    "selected_agents",
                    []
                ),

            "intent":
                llm_plan.get(
                    "intent",
                    "Marine ecosystem analysis"
                ),

            "complexity":
                llm_plan.get(
                    "complexity",
                    "moderate"
                ),

            "reason":
                llm_plan.get(
                    "reason",
                    ""
                ),

            "planning_fallback":
                llm_plan.get(
                    "llm_planning_failed",
                    False
                ),

            "synthesis_available":
                bool(
                    llm_synthesis.get(
                        "answer"
                    )
                )
        },

        # ----------------------------------------------------
        # LLM PLAN
        # ----------------------------------------------------

        "llm_plan": llm_plan,

        # ----------------------------------------------------
        # LLM SYNTHESIS
        # ----------------------------------------------------

        "llm_synthesis": llm_synthesis,

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        "data_status": {

            "sea_surface_temperature_available":
                temperature is not None,

            "chlorophyll_available":
                chlorophyll is not None,

            "historical_observation": True
        },

        # ----------------------------------------------------
        # PLANNING
        # ----------------------------------------------------

        "planner":
            planner_result,

        "query_router":
            router_result,

        "execution_plan":
            execution_plan,

        # ----------------------------------------------------
        # OBSERVATIONS
        # ----------------------------------------------------

        "observations":
            observations,

        # ----------------------------------------------------
        # AGENT RESULTS
        # ----------------------------------------------------

        "fish_analysis":
            fish_result,

        "ocean_analysis":
            ocean_result,

        "ecosystem_analysis":
            ecosystem_result,

        "weather_analysis":
            weather_result,

        "risk_analysis":
            risk_result,

        "uncertainty_analysis":
            uncertainty_result,

        "evidence":
            evidence_result,

        "agent_debate":
            debate_result,

        "reasoning":
            reasoning_result,

        "causal_reasoning":
            causal_result,

        "decision":
            decision_result,

        "alerts":
            alerts_result,

        "visualization":
            visualization_result,

        "report":
            report_result,

        # ----------------------------------------------------
        # PFZ / ROUTE / GEOFENCE
        # ----------------------------------------------------

        "pfz_analysis":
            pfz_result,

        "route_analysis":
            route_result,

        "geofence_analysis":
            geofence_result,

        # ----------------------------------------------------
        # DATA SOURCES
        # ----------------------------------------------------

        "data_sources": {

            "marine": [
                "NOAA CoastWatch MUR SST",
                "INCOIS Oceansat-2 OCM"
            ],

            "weather": (
                ["Open-Meteo"]
                if weather_data
                else []
            )
        },

        # ----------------------------------------------------
        # SCIENTIFIC NOTE
        # ----------------------------------------------------

        "historical_data_note": (
            "Marine ecosystem observations are evaluated "
            "using the requested observation date. "
            "These observations must not be interpreted "
            "as current conditions unless the underlying "
            "source provides current data."
        ),

        "scientific_note": (
            "ORCA combines external observations, "
            "specialist agent analysis, scientific evidence, "
            "uncertainty and LLM-assisted orchestration. "
            "Environmental associations are treated as "
            "evidence-informed hypotheses rather than "
            "automatic proof of causation."
        ),

        "system_status":
            "LLM-orchestrated ORCA analysis completed"
    }


# ============================================================
# CHAT INTERFACE
# ============================================================

def run_orca_chat(
    query,
    species=DEFAULT_SPECIES,
    lat=9.5,
    lon=76.0,
    date=None,
    salinity=34
):
    """
    Convert structured ORCA analysis into a
    human-readable chatbot response.

    If Gemini synthesis is available, it is used as the
    conversational response. The structured ORCA analysis
    remains available underneath it.
    """

    result = run_agentic_orca(
        query=query,
        species=species,
        lat=lat,
        lon=lon,
        date=date,
        salinity=salinity
    )

    # --------------------------------------------------------
    # Prefer LLM-generated answer
    # --------------------------------------------------------

    llm_synthesis = safe_dict(
        result.get(
            "llm_synthesis"
        )
    )

    llm_answer = str(
        llm_synthesis.get(
            "answer",
            ""
        )
    ).strip()

    if llm_answer:

        return {
            "query": query,

            "response": llm_answer,

            "analysis": result,

            "llm_used": bool(
                llm_synthesis.get(
                    "llm_used",
                    False
                )
            ),

            "model": llm_synthesis.get(
                "model"
            )
        }

    # --------------------------------------------------------
    # Fallback structured response
    # --------------------------------------------------------

    risk = safe_dict(
        result.get(
            "risk_analysis"
        )
    ).get(
        "overall_risk",
        "Unknown"
    )

    uncertainty = safe_dict(
        result.get(
            "uncertainty_analysis"
        )
    ).get(
        "uncertainty_level",
        "Unknown"
    )

    confidence = safe_dict(
        result.get(
            "uncertainty_analysis"
        )
    ).get(
        "confidence"
    )

    temperature = safe_dict(
        result.get(
            "observations"
        )
    ).get(
        "sea_surface_temperature"
    )

    chlorophyll = safe_dict(
        result.get(
            "observations"
        )
    ).get(
        "chlorophyll"
    )

    salinity_value = safe_dict(
        result.get(
            "observations"
        )
    ).get(
        "salinity"
    )

    response = []

    response.append(
        "🐋 ORCA Marine Ecosystem Intelligence"
    )

    response.append(
        f"🐟 Species: {species}"
    )

    response.append(
        f"📍 Location: {lat}, {lon}"
    )

    response.append(
        f"📅 Observation Date: "
        f"{result.get('date', 'Unknown')}"
    )

    response.append(
        f"⚠️ Overall Environmental Risk: {risk}"
    )

    response.append(
        f"🔬 Uncertainty: {uncertainty}"
    )

    if confidence is not None:

        response.append(
            f"📊 Data Confidence: {confidence}%"
        )

    response.append("")

    # --------------------------------------------------------
    # Observations
    # --------------------------------------------------------

    response.append(
        "🌊 Environmental Observations:"
    )

    if temperature is not None:

        response.append(
            f"• 🌡️ Sea Surface Temperature: "
            f"{temperature:.2f} °C"
        )

    else:

        response.append(
            "• 🌡️ Sea Surface Temperature: "
            "Data unavailable"
        )

    if chlorophyll is not None:

        response.append(
            f"• 🌿 Chlorophyll: "
            f"{chlorophyll:.3f}"
        )

    else:

        response.append(
            "• 🌿 Chlorophyll: "
            "Data unavailable"
        )

    if salinity_value is not None:

        response.append(
            f"• 🧂 Salinity: "
            f"{salinity_value:.2f} PSU"
        )

    response.append("")

    # --------------------------------------------------------
    # Reasoning
    # --------------------------------------------------------

    response.append(
        "🧠 ORCA Reasoning:"
    )

    reasoning = safe_dict(
        result.get(
            "reasoning"
        )
    )

    for reason in safe_list(
        reasoning.get(
            "reasoning",
            []
        )
    ):

        response.append(
            f"• {reason}"
        )

    response.append("")

    # --------------------------------------------------------
    # Causal reasoning
    # --------------------------------------------------------

    response.append(
        "🔗 Causal Pathway:"
    )

    causal = safe_dict(
        result.get(
            "causal_reasoning"
        )
    )

    causal_chain = safe_list(
        causal.get(
            "causal_chain",
            []
        )
    )

    for index, item in enumerate(
        causal_chain,
        start=1
    ):

        if isinstance(
            item,
            dict
        ):

            factor = item.get(
                "factor",
                "Unknown factor"
            )

            effect = item.get(
                "effect",
                "Unknown effect"
            )

            response.append(
                f"{index}. {factor} → {effect}"
            )

        else:

            response.append(
                f"{index}. {item}"
            )

    response.append("")

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    response.append(
        "🔎 Research Evidence:"
    )

    evidence_container = safe_dict(
        result.get(
            "evidence"
        )
    )

    evidence_items = safe_list(
        evidence_container.get(
            "evidence",
            []
        )
    )

    if evidence_items:

        for index, item in enumerate(
            evidence_items,
            start=1
        ):

            item = safe_dict(
                item
            )

            finding = item.get(
                "finding",
                "Evidence finding unavailable"
            )

            source = item.get(
                "source",
                "Unknown source"
            )

            response.append(
                f"{index}. {finding}"
            )

            response.append(
                f"   📄 Source: {source}"
            )

            if item.get(
                "evidence_type"
            ):

                response.append(
                    f"   🧪 Evidence type: "
                    f"{item.get('evidence_type')}"
                )

            if item.get(
                "relevance"
            ):

                response.append(
                    f"   🎯 Relevance: "
                    f"{item.get('relevance')}"
                )

    else:

        response.append(
            "• No matching research evidence found."
        )

    response.append("")

    # --------------------------------------------------------
    # Debate
    # --------------------------------------------------------

    response.append(
        "⚔️ Multi-Agent Assessment:"
    )

    debate = safe_dict(
        result.get(
            "agent_debate"
        )
    )

    if debate.get(
        "disagreement_detected"
    ):

        response.append(
            "• Agent disagreement detected."
        )

        explanation = debate.get(
            "explanation",
            ""
        )

        if explanation:

            response.append(
                f"• {explanation}"
            )

    else:

        response.append(
            "• Specialist agents show broadly "
            "consistent environmental assessment."
        )

    response.append("")

    # --------------------------------------------------------
    # Scientific limitations
    # --------------------------------------------------------

    response.append(
        "⚠️ Scientific Limitation:"
    )

    response.append(
        "• ORCA identifies environmental signals "
        "associated with ecosystem stress."
    )

    response.append(
        "• These relationships are evidence-informed "
        "hypotheses and do not establish direct causation."
    )

    response.append(
        "• Environmental risk does not directly "
        "represent fish abundance, biomass or "
        "catch probability."
    )

    response.append("")

    # --------------------------------------------------------
    # Decision warnings
    # --------------------------------------------------------

    decision = safe_dict(
        result.get(
            "decision"
        )
    )

    warnings = safe_list(
        decision.get(
            "warnings",
            []
        )
    )

    if warnings:

        response.append(
            "⚠️ Decision Warnings:"
        )

        for warning in warnings:

            response.append(
                f"• {warning}"
            )

        response.append("")

    response.append(
        "📊 ORCA combined specialist agents, "
        "marine observations, research evidence, "
        "uncertainty analysis and LLM orchestration."
    )

    return {
        "query": query,

        "response":
            "\n".join(
                response
            ),

        "analysis":
            result,

        "llm_used":
            False,

        "model":
            None
    }


# ============================================================
# SPATIAL PFZ ANALYSIS
# ============================================================

def run_spatial_pfz(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    date,
    step=0.2
):
    """
    Run spatial Potential Fishing Zone analysis.
    """

    marine_data = get_spatial_marine_data(
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        date=date,
        step=step
    )

    pfz_result = analyze_spatial_pfz(
        marine_data
    )

    return {
        "project": "ORCA",

        "analysis_type": (
            "Spatial Potential Fishing Zone Analysis"
        ),

        "date": date,

        "bounds": {
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_lon": min_lon,
            "max_lon": max_lon
        },

        "pfz_analysis":
            pfz_result,

        "system_status":
            "Spatial PFZ analysis completed"
    }


# ============================================================
# ROUTE ANALYSIS
# ============================================================

def run_route_analysis(
    start_lat,
    start_lon,
    end_lat,
    end_lon
):
    """
    Analyze route safety using marine weather data.
    """

    weather_data = get_weather_data(
        start_lat,
        start_lon
    )

    weather_code = weather_data.get(
        "weather_code"
    )

    weather_condition = weather_code_to_condition(
        weather_code
    )

    route_result = analyze_route(
        start_lat=start_lat,
        start_lon=start_lon,

        end_lat=end_lat,
        end_lon=end_lon,

        wind_speed=(
            weather_data.get(
                "wind_speed"
            ) or 0
        ),

        wave_height=(
            weather_data.get(
                "wave_height"
            ) or 0
        ),

        rainfall=(
            weather_data.get(
                "rainfall"
            ) or 0
        ),

        weather_condition=
            weather_condition
    )

    alerts_result = generate_alerts(
        wind_speed=weather_data.get(
            "wind_speed"
        ),

        wave_height=weather_data.get(
            "wave_height"
        ),

        rainfall=weather_data.get(
            "rainfall"
        ),

        weather_condition=
            weather_condition,

        route_result=
            route_result
    )

    return {
        "project": "ORCA",

        "route_analysis":
            route_result,

        "weather":
            weather_data,

        "alerts":
            alerts_result,

        "system_status":
            "Route safety analysis completed"
    }


# ============================================================
# GEOFENCE ANALYSIS
# ============================================================

def run_geofence_analysis(
    route_points,
    restricted_zones
):
    """
    Check route points against restricted marine zones.
    """

    geofence_result = analyze_geofence(
        route_points=route_points,
        restricted_zones=restricted_zones
    )

    alerts_result = generate_alerts(
        wind_speed=None,
        wave_height=None,
        rainfall=None,
        weather_condition="Unknown",
        geofence_result=geofence_result
    )

    return {
        "project": "ORCA",

        "geofence_analysis":
            geofence_result,

        "alerts":
            alerts_result,

        "system_status":
            "Geofence analysis completed"
    }


# ============================================================
# MARINE SAFETY DECISION
# ============================================================

def run_safety_decision(
    query,
    lat,
    lon,
    wind_speed=None,
    wave_height=None,
    rainfall=None,
    weather_condition="Unknown"
):
    """
    Run marine safety decision support.
    """

    if wind_speed is None:
        wind_speed = 0

    if wave_height is None:
        wave_height = 0

    if rainfall is None:
        rainfall = 0

    weather_result = analyze_weather(
        wind_speed=wind_speed,
        wave_height=wave_height,
        rainfall=rainfall,
        weather_condition=weather_condition
    )

    route_result = None

    alerts_result = generate_alerts(
        wind_speed=wind_speed,
        wave_height=wave_height,
        rainfall=rainfall,
        weather_condition=weather_condition
    )

    return {
        "query": query,

        "location": {
            "latitude": lat,
            "longitude": lon
        },

        "weather_analysis":
            weather_result,

        "route_analysis":
            route_result,

        "alerts":
            alerts_result,

        "decision": (
            "Marine safety assessment completed using "
            "weather and environmental conditions."
        ),

        "scientific_note": (
            "This is a decision-support assessment and does not "
            "replace official marine warnings or professional "
            "navigation judgment."
        )
    }


# ============================================================
# ALERT ANALYSIS
# ============================================================

def run_alert_analysis(
    query,
    lat,
    lon,
    wind_speed=None,
    wave_height=None,
    rainfall=None,
    weather_condition="Unknown"
):
    """
    Run ORCA alert analysis.
    """

    if wind_speed is None:
        wind_speed = 0

    if wave_height is None:
        wave_height = 0

    if rainfall is None:
        rainfall = 0

    alert_result = generate_alerts(
        wind_speed=wind_speed,
        wave_height=wave_height,
        rainfall=rainfall,
        weather_condition=weather_condition
    )

    return {
        "query": query,

        "location": {
            "latitude": lat,
            "longitude": lon
        },

        "alert_analysis":
            alert_result,

        "alerts":
            alert_result.get(
                "alerts",
                []
            ),

        "overall_level":
            alert_result.get(
                "overall_level",
                "Low"
            ),

        "scientific_note": (
            "ORCA alerts are automated decision-support signals "
            "based on available marine and weather conditions. "
            "Official marine warnings should take priority."
        )
    }
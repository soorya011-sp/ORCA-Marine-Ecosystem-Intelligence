def plan_query(query):
    query_lower = query.lower()

    agents = []
    intent = "general_marine_information"

    # Fish-related questions
    if any(word in query_lower for word in [
        "fish",
        "sardine",
        "productivity",
        "fishing",
        "fishing zone",
        "pfz"
    ]):
        agents.append("Fish Agent")
        intent = "fish_analysis"

    # Ocean-related questions
    if any(word in query_lower for word in [
        "temperature",
        "sst",
        "chlorophyll",
        "salinity",
        "ocean",
        "sea condition"
    ]):
        agents.append("Ocean Agent")

    # Weather / safety questions
    if any(word in query_lower for word in [
        "weather",
        "safe",
        "safety",
        "storm",
        "cyclone",
        "lightning",
        "wave",
        "waves"
    ]):
        agents.append("Safety Agent")

    # Route questions
    if any(word in query_lower for word in [
        "route",
        "navigation",
        "navigate",
        "travel"
    ]):
        agents.append("Geospatial Agent")

    # Research / explanation
    if any(word in query_lower for word in [
        "why",
        "reason",
        "research",
        "evidence",
        "study",
        "paper"
    ]):
        agents.append("Research Agent")

    # Always use reasoning
    agents.append("Reasoning Agent")

    # Remove duplicates
    agents = list(dict.fromkeys(agents))

    return {
        "query": query,
        "intent": intent,
        "selected_agents": agents,
        "planning_complete": True
    }


def build_execution_plan(query):
    """
    Convert the planner result into an execution plan
    for the ORCA multi-agent controller.
    """

    planning = plan_query(query)

    selected_agents = planning.get("selected_agents", [])

    execution_steps = []

    # Data collection first
    execution_steps.append("Marine Data Retrieval")

    # Specialist agents
    for agent in selected_agents:
        execution_steps.append(agent)

    # Core ORCA reasoning pipeline
    execution_steps.extend([
        "Risk Agent",
        "Uncertainty Agent",
        "Evidence Agent",
        "Debate Agent",
        "Causal Reasoning Agent",
        "Decision Agent",
        "Visualization Agent",
        "Alert Agent",
        "Report Agent"
    ])

    # Remove duplicates while preserving order
    execution_steps = list(dict.fromkeys(execution_steps))

    return {
        "query": query,
        "intent": planning.get("intent"),
        "selected_agents": selected_agents,
        "execution_steps": execution_steps,
        "planning_complete": True,
        "execution_plan_complete": True
    }


if __name__ == "__main__":

    query = "Why has fish productivity declined near Kerala?"

    print("PLANNER RESULT")
    print(plan_query(query))

    print("\nEXECUTION PLAN")
    print(build_execution_plan(query))
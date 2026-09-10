import React, { useState } from "react";
import {
  Send,
  User,
  Bot,
  Loader2,
  Brain,
  Fish,
  Waves,
  CloudSun,
  Map,
  ShieldAlert,
  BookOpen,
  AlertTriangle,
  CheckCircle,
  Activity,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

export default function AskORCA() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const suggestedQuestions = [
    "Why has Indian oil sardine productivity declined?",
    "Analyze the ocean conditions for Indian oil sardine",
    "What are the current marine safety conditions?",
    "Find potential fishing zones",
    "Why is fish productivity changing?",
    "Analyze the marine ecosystem",
  ];

  const askORCA = async (userQuery = query) => {
    const cleanQuery = userQuery.trim();

    if (!cleanQuery || loading) {
      return;
    }

    setError("");
    setLoading(true);

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: cleanQuery,
      },
    ]);

    setQuery("");

    try {
      const params = new URLSearchParams({
        query: cleanQuery,
        species: "Indian Oil Sardine",
        temperature: "30",
        chlorophyll: "0.3",
        salinity: "34",
      });

      const response = await fetch(
        `${API_URL}/agentic-orca?${params.toString()}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Backend returned HTTP ${response.status}`
        );
      }

      const data = await response.json();

      const plan = data.plan || {};
      const routing = data.routing || {};
      const executionPlan = data.execution_plan || {};
      const agents = data.agent_results || {};

      const reasoning =
        agents.reasoning ||
        data.reasoning ||
        {};

      const causal =
        agents.causal_reasoning ||
        agents.causal_reasoning_agent ||
        data.causal_reasoning ||
        {};

      const uncertainty =
        agents.uncertainty ||
        data.uncertainty ||
        {};

      const debate =
        agents.debate ||
        data.debate ||
        {};

      const evidence =
        agents.evidence ||
        data.evidence ||
        {};

      const decision =
        agents.decision ||
        data.decision ||
        {};

      const ecosystem =
        agents.ecosystem ||
        data.ecosystem ||
        {};

      const fish =
        agents.fish ||
        data.fish ||
        {};

      const ocean =
        agents.ocean ||
        data.ocean ||
        {};

      const weather =
        agents.weather ||
        data.weather ||
        {};

      const pfz =
        agents.pfz ||
        agents.pfz_spatial ||
        data.pfz ||
        {};

      const route =
        agents.route ||
        data.route ||
        {};

      const geofence =
        agents.geofence ||
        data.geofence ||
        {};

      const alerts =
        agents.alerts ||
        data.alerts ||
        {};

      setMessages((prev) => [
        ...prev,
        {
          type: "orca",
          text: buildMainAnswer(data, reasoning, decision),
          data: {
            plan,
            routing,
            executionPlan,
            agents,
            reasoning,
            causal,
            uncertainty,
            debate,
            evidence,
            decision,
            ecosystem,
            fish,
            ocean,
            weather,
            pfz,
            route,
            geofence,
            alerts,
          },
        },
      ]);
    } catch (err) {
      console.error("ORCA error:", err);

      setError(
        err.message ||
          "Unable to connect to the ORCA backend."
      );

      setMessages((prev) => [
        ...prev,
        {
          type: "error",
          text:
            "ORCA could not process this request. Please make sure the FastAPI backend is running on port 8000.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const buildMainAnswer = (
    data,
    reasoning,
    decision
  ) => {
    if (decision?.decision?.length) {
      return decision.decision.join(" ");
    }

    if (reasoning?.reasoning?.length) {
      return reasoning.reasoning.join(" ");
    }

    if (data?.final_answer) {
      return data.final_answer;
    }

    if (data?.answer) {
      return data.answer;
    }

    return "ORCA completed the requested marine ecosystem analysis.";
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    askORCA();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">

        {/* HEADER */}
        <div className="mb-6 flex flex-col gap-4 rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-xl backdrop-blur sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-500/10">
              <Bot className="h-7 w-7 text-cyan-400" />
            </div>

            <div>
              <h1 className="text-2xl font-bold tracking-tight">
                Ask ORCA
              </h1>

              <p className="text-sm text-slate-400">
                Marine Ecosystem Reasoning with Collaborative Agents
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            ORCA Online
          </div>
        </div>

        {/* CHAT AREA */}
        <div className="flex-1 overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-2xl">

          {/* EMPTY STATE */}
          {messages.length === 0 && (
            <div className="flex min-h-[520px] flex-col items-center justify-center px-5 py-12 text-center">
              <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-cyan-500/10">
                <Brain className="h-10 w-10 text-cyan-400" />
              </div>

              <h2 className="mb-3 text-3xl font-bold">
                How can ORCA help?
              </h2>

              <p className="mb-8 max-w-2xl text-slate-400">
                Ask questions about fish productivity, ocean
                conditions, marine ecosystems, fishing zones,
                weather, safety and environmental risks.
              </p>

              <div className="grid w-full max-w-4xl gap-3 sm:grid-cols-2">
                {suggestedQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => askORCA(question)}
                    className="rounded-xl border border-slate-700 bg-slate-800/60 p-4 text-left text-sm text-slate-300 transition hover:border-cyan-500/50 hover:bg-slate-800 hover:text-white"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* MESSAGES */}
          {messages.length > 0 && (
            <div className="max-h-[calc(100vh-280px)] min-h-[500px] overflow-y-auto p-4 sm:p-6">
              <div className="mx-auto max-w-5xl space-y-6">

                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex gap-3 ${
                      message.type === "user"
                        ? "justify-end"
                        : "justify-start"
                    }`}
                  >

                    {/* ORCA */}
                    {message.type !== "user" && (
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10">
                        {message.type === "error" ? (
                          <AlertTriangle className="h-5 w-5 text-red-400" />
                        ) : (
                          <Bot className="h-5 w-5 text-cyan-400" />
                        )}
                      </div>
                    )}

                    {/* MESSAGE */}
                    <div
                      className={`max-w-[85%] rounded-2xl p-4 ${
                        message.type === "user"
                          ? "bg-cyan-600 text-white"
                          : message.type === "error"
                          ? "border border-red-500/20 bg-red-500/10 text-red-300"
                          : "border border-slate-700 bg-slate-800/80 text-slate-200"
                      }`}
                    >
                      <div className="whitespace-pre-wrap text-sm leading-7">
                        {message.text}
                      </div>

                      {message.type === "orca" &&
                        message.data && (
                          <ORCAAnalysis data={message.data} />
                        )}
                    </div>

                    {/* USER */}
                    {message.type === "user" && (
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-700">
                        <User className="h-5 w-5 text-slate-300" />
                      </div>
                    )}
                  </div>
                ))}

                {/* LOADING */}
                {loading && (
                  <div className="flex gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10">
                      <Bot className="h-5 w-5 text-cyan-400" />
                    </div>

                    <div className="rounded-2xl border border-slate-700 bg-slate-800/80 px-5 py-4">
                      <div className="flex items-center gap-3">
                        <Loader2 className="h-5 w-5 animate-spin text-cyan-400" />

                        <span className="text-sm text-slate-400">
                          ORCA agents are analyzing the request...
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* ERROR */}
          {error && (
            <div className="mx-4 mb-3 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-300 sm:mx-6">
              {error}
            </div>
          )}

          {/* INPUT */}
          <div className="border-t border-slate-800 bg-slate-950/70 p-4">
            <form
              onSubmit={handleSubmit}
              className="mx-auto flex max-w-5xl gap-3"
            >
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
                placeholder="Ask ORCA about the marine ecosystem..."
                className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-500"
              />

              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="flex items-center justify-center gap-2 rounded-xl bg-cyan-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {loading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Send className="h-5 w-5" />
                )}

                <span className="hidden sm:inline">
                  Ask
                </span>
              </button>
            </form>

            <p className="mx-auto mt-2 max-w-5xl text-xs text-slate-600">
              ORCA provides evidence-grounded marine decision support.
              It does not replace official marine advisories or professional judgment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}


/* =========================================================
   ORCA ANALYSIS
========================================================= */

function ORCAAnalysis({ data }) {
  const {
    plan,
    routing,
    executionPlan,
    agents,
    reasoning,
    causal,
    uncertainty,
    debate,
    evidence,
    decision,
    ecosystem,
    fish,
    ocean,
    weather,
    pfz,
    route,
    geofence,
    alerts,
  } = data;

  return (
    <div className="mt-5 space-y-4 border-t border-slate-700 pt-5">

      {/* AGENTS */}
      <Section
        title="Collaborative Agents"
        icon={<Brain className="h-4 w-4" />}
      >
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {getAgentNames(agents).map((agent, index) => (
            <div
              key={index}
              className="flex items-center gap-2 rounded-lg border border-slate-700 bg-slate-900/70 px-3 py-2 text-xs text-slate-300"
            >
              <CheckCircle className="h-4 w-4 text-emerald-400" />
              {formatAgentName(agent)}
            </div>
          ))}
        </div>
      </Section>

      {/* PLANNER */}
      {(plan?.selected_agents?.length ||
        routing?.routes?.length ||
        executionPlan?.execution_order?.length) && (
        <Section
          title="ORCA Planning"
          icon={<Activity className="h-4 w-4" />}
        >
          {plan?.intent && (
            <p className="mb-2 text-sm text-slate-300">
              <span className="text-slate-500">Intent:</span>{" "}
              {plan.intent}
            </p>
          )}

          {routing?.routes?.length > 0 && (
            <p className="text-sm text-slate-300">
              <span className="text-slate-500">
                Detected domains:
              </span>{" "}
              {routing.routes.join(", ")}
            </p>
          )}

          {executionPlan?.execution_order?.length > 0 && (
            <p className="mt-2 text-sm text-slate-300">
              <span className="text-slate-500">
                Execution:
              </span>{" "}
              {executionPlan.execution_order.join(" → ")}
            </p>
          )}
        </Section>
      )}

      {/* FISH */}
      {Object.keys(fish || {}).length > 0 && (
        <Section
          title="Fish Analysis"
          icon={<Fish className="h-4 w-4" />}
        >
          {fish.species && (
            <InfoRow
              label="Species"
              value={fish.species}
            />
          )}

          {fish.risk && (
            <InfoRow
              label="Fish risk"
              value={fish.risk}
            />
          )}

          {fish.risk_factors?.length > 0 && (
            <ListBlock
              title="Risk factors"
              items={fish.risk_factors}
            />
          )}
        </Section>
      )}

      {/* OCEAN */}
      {Object.keys(ocean || {}).length > 0 && (
        <Section
          title="Ocean Conditions"
          icon={<Waves className="h-4 w-4" />}
        >
          {ocean.temperature !== undefined && (
            <InfoRow
              label="Sea surface temperature"
              value={`${ocean.temperature} °C`}
            />
          )}

          {ocean.chlorophyll !== undefined && (
            <InfoRow
              label="Chlorophyll"
              value={ocean.chlorophyll}
            />
          )}

          {ocean.salinity !== undefined && (
            <InfoRow
              label="Salinity"
              value={ocean.salinity}
            />
          )}

          {ocean.ocean_condition && (
            <InfoRow
              label="Ocean condition"
              value={ocean.ocean_condition}
            />
          )}

          {ocean.interpretation && (
            <p className="mt-3 text-sm leading-6 text-slate-400">
              {ocean.interpretation}
            </p>
          )}
        </Section>
      )}

      {/* ECOSYSTEM */}
      {Object.keys(ecosystem || {}).length > 0 && (
        <Section
          title="Ecosystem Assessment"
          icon={<Activity className="h-4 w-4" />}
        >
          {ecosystem.ecosystem_status && (
            <InfoRow
              label="Status"
              value={ecosystem.ecosystem_status}
            />
          )}

          {ecosystem.factors?.length > 0 && (
            <ListBlock
              title="Observed factors"
              items={ecosystem.factors}
            />
          )}
        </Section>
      )}

      {/* WEATHER */}
      {Object.keys(weather || {}).length > 0 && (
        <Section
          title="Weather & Marine Safety"
          icon={<CloudSun className="h-4 w-4" />}
        >
          {weather.wind_speed !== undefined && (
            <InfoRow
              label="Wind speed"
              value={`${weather.wind_speed} km/h`}
            />
          )}

          {weather.wave_height !== undefined && (
            <InfoRow
              label="Wave height"
              value={`${weather.wave_height} m`}
            />
          )}

          {weather.rainfall !== undefined && (
            <InfoRow
              label="Rainfall"
              value={`${weather.rainfall} mm`}
            />
          )}

          {weather.weather_condition && (
            <InfoRow
              label="Condition"
              value={weather.weather_condition}
            />
          )}

          {weather.safety_risk && (
            <InfoRow
              label="Safety risk"
              value={weather.safety_risk}
            />
          )}

          {weather.risks?.length > 0 && (
            <ListBlock
              title="Weather risks"
              items={weather.risks}
            />
          )}
        </Section>
      )}

      {/* PFZ */}
      {Object.keys(pfz || {}).length > 0 && (
        <Section
          title="Potential Fishing Zone"
          icon={<Map className="h-4 w-4" />}
        >
          {pfz.high_potential_zones !== undefined && (
            <InfoRow
              label="High-potential zones"
              value={pfz.high_potential_zones}
            />
          )}

          {pfz.moderate_potential_zones !== undefined && (
            <InfoRow
              label="Moderate zones"
              value={pfz.moderate_potential_zones}
            />
          )}

          {pfz.average_pfz_score !== undefined &&
            pfz.average_pfz_score !== null && (
              <InfoRow
                label="Average PFZ score"
                value={pfz.average_pfz_score}
              />
            )}

          {pfz.best_zone && (
            <div className="mt-3 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-3">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-cyan-400">
                Best detected zone
              </p>

              <p className="text-sm text-slate-300">
                Latitude:{" "}
                {pfz.best_zone.latitude}
              </p>

              <p className="text-sm text-slate-300">
                Longitude:{" "}
                {pfz.best_zone.longitude}
              </p>

              <p className="text-sm text-slate-300">
                PFZ score:{" "}
                {pfz.best_zone.pfz_score}
              </p>
            </div>
          )}

          {pfz.scientific_note && (
            <p className="mt-3 text-xs leading-5 text-slate-500">
              {pfz.scientific_note}
            </p>
          )}
        </Section>
      )}

      {/* ROUTE */}
      {Object.keys(route || {}).length > 0 && (
        <Section
          title="Route Analysis"
          icon={<Map className="h-4 w-4" />}
        >
          {route.distance_km !== undefined && (
            <InfoRow
              label="Distance"
              value={`${route.distance_km} km`}
            />
          )}

          {route.safety?.safety && (
            <InfoRow
              label="Route safety"
              value={route.safety.safety}
            />
          )}

          {route.recommendation && (
            <p className="mt-3 text-sm leading-6 text-slate-400">
              {route.recommendation}
            </p>
          )}
        </Section>
      )}

      {/* GEOFENCE */}
      {Object.keys(geofence || {}).length > 0 && (
        <Section
          title="Geofence Analysis"
          icon={<ShieldAlert className="h-4 w-4" />}
        >
          {geofence.status && (
            <InfoRow
              label="Status"
              value={geofence.status}
            />
          )}

          {geofence.violations?.length > 0 && (
            <ListBlock
              title="Detected violations"
              items={geofence.violations.map(
                (item) =>
                  `${item.zone}: ${item.reason}`
              )}
            />
          )}

          {geofence.recommendation && (
            <p className="mt-3 text-sm text-slate-400">
              {geofence.recommendation}
            </p>
          )}
        </Section>
      )}

      {/* ALERTS */}
      {Object.keys(alerts || {}).length > 0 && (
        <Section
          title="Marine Alerts"
          icon={<AlertTriangle className="h-4 w-4" />}
        >
          {alerts.overall_level && (
            <InfoRow
              label="Overall alert level"
              value={alerts.overall_level}
            />
          )}

          {alerts.alert_count !== undefined && (
            <InfoRow
              label="Alert count"
              value={alerts.alert_count}
            />
          )}

          {alerts.alerts?.length > 0 && (
            <div className="mt-3 space-y-2">
              {alerts.alerts.map((alert, index) => (
                <div
                  key={index}
                  className="rounded-xl border border-slate-700 bg-slate-900/70 p-3"
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-sm font-semibold text-slate-200">
                      {alert.type}
                    </span>

                    <span className="rounded-full bg-slate-700 px-2 py-1 text-xs text-slate-300">
                      {alert.level}
                    </span>
                  </div>

                  <p className="mt-2 text-xs leading-5 text-slate-400">
                    {alert.message}
                  </p>
                </div>
              ))}
            </div>
          )}
        </Section>
      )}

      {/* CAUSAL REASONING */}
      {causal?.causal_chain?.length > 0 && (
        <Section
          title="Causal Reasoning"
          icon={<Brain className="h-4 w-4" />}
        >
          <div className="space-y-3">
            {causal.causal_chain.map(
              (item, index) => (
                <div
                  key={index}
                  className="rounded-xl border border-slate-700 bg-slate-900/70 p-3"
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs text-cyan-400">
                      {index + 1}
                    </div>

                    <div>
                      <p className="text-sm font-medium text-slate-200">
                        {item.factor}
                      </p>

                      <p className="mt-1 text-xs text-slate-400">
                        ↓ {item.effect}
                      </p>

                      {item.confidence && (
                        <p className="mt-2 text-xs text-cyan-400">
                          Confidence:{" "}
                          {item.confidence}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )
            )}
          </div>

          {causal.alternative_explanations?.length > 0 && (
            <ListBlock
              title="Alternative explanations"
              items={causal.alternative_explanations}
            />
          )}

          {causal.causal_inference_warning && (
            <p className="mt-3 rounded-lg border border-amber-500/20 bg-amber-500/5 p-3 text-xs leading-5 text-amber-300">
              {causal.causal_inference_warning}
            </p>
          )}
        </Section>
      )}

      {/* DEBATE */}
      {Object.keys(debate || {}).length > 0 && (
        <Section
          title="Agent Debate"
          icon={<Brain className="h-4 w-4" />}
        >
          {debate.agent_opinions && (
            <div className="space-y-2">
              {Object.entries(
                debate.agent_opinions
              ).map(([agent, opinion]) => (
                <InfoRow
                  key={agent}
                  label={agent}
                  value={opinion}
                />
              ))}
            </div>
          )}

          {debate.disagreement_detected !== undefined && (
            <div className="mt-3 flex items-center gap-2 text-sm">
              {debate.disagreement_detected ? (
                <>
                  <AlertTriangle className="h-4 w-4 text-amber-400" />
                  <span className="text-amber-300">
                    Specialist agents disagree.
                  </span>
                </>
              ) : (
                <>
                  <CheckCircle className="h-4 w-4 text-emerald-400" />
                  <span className="text-emerald-300">
                    Specialist agents agree.
                  </span>
                </>
              )}
            </div>
          )}

          {debate.explanation && (
            <p className="mt-3 text-xs leading-5 text-slate-500">
              {debate.explanation}
            </p>
          )}
        </Section>
      )}

      {/* EVIDENCE */}
      {Object.keys(evidence || {}).length > 0 && (
        <Section
          title="Research Evidence"
          icon={<BookOpen className="h-4 w-4" />}
        >
          {evidence.evidence?.length > 0 ? (
            <div className="space-y-3">
              {evidence.evidence.map(
                (item, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-slate-700 bg-slate-900/70 p-3"
                  >
                    <p className="text-sm font-medium text-slate-200">
                      {item.title}
                    </p>

                    {item.finding && (
                      <p className="mt-2 text-xs leading-5 text-slate-400">
                        {item.finding}
                      </p>
                    )}

                    {item.relevance_score !== undefined && (
                      <p className="mt-2 text-xs text-cyan-400">
                        Relevance score:{" "}
                        {item.relevance_score}
                      </p>
                    )}
                  </div>
                )
              )}
            </div>
          ) : (
            <p className="text-sm text-slate-500">
              No supporting research evidence was returned.
            </p>
          )}
        </Section>
      )}

      {/* UNCERTAINTY */}
      {Object.keys(uncertainty || {}).length > 0 && (
        <Section
          title="Confidence & Uncertainty"
          icon={<Activity className="h-4 w-4" />}
        >
          {uncertainty.confidence !== undefined && (
            <InfoRow
              label="Confidence"
              value={`${uncertainty.confidence}%`}
            />
          )}

          {uncertainty.uncertainty_level && (
            <InfoRow
              label="Uncertainty"
              value={uncertainty.uncertainty_level}
            />
          )}

          {uncertainty.uncertainty_reasons?.length > 0 && (
            <ListBlock
              title="Why uncertainty exists"
              items={uncertainty.uncertainty_reasons}
            />
          )}
        </Section>
      )}

      {/* FINAL DECISION */}
      {Object.keys(decision || {}).length > 0 && (
        <Section
          title="ORCA Final Decision"
          icon={<CheckCircle className="h-4 w-4" />}
        >
          {decision.overall_risk && (
            <InfoRow
              label="Overall risk"
              value={decision.overall_risk}
            />
          )}

          {decision.alert_level && (
            <InfoRow
              label="Alert level"
              value={decision.alert_level}
            />
          )}

          {decision.decision?.length > 0 && (
            <ListBlock
              title="Decision"
              items={decision.decision}
            />
          )}

          {decision.warnings?.length > 0 && (
            <ListBlock
              title="Warnings"
              items={decision.warnings}
            />
          )}
        </Section>
      )}

      {/* GENERAL REASONING */}
      {reasoning?.reasoning?.length > 0 && (
        <Section
          title="ORCA Reasoning"
          icon={<Brain className="h-4 w-4" />}
        >
          <ListBlock
            title="Reasoning"
            items={reasoning.reasoning}
          />

          {reasoning.causal_chain?.length > 0 && (
            <div className="mt-3">
              <ListBlock
                title="Reasoning chain"
                items={reasoning.causal_chain}
              />
            </div>
          )}
        </Section>
      )}

    </div>
  );
}


/* =========================================================
   UI COMPONENTS
========================================================= */

function Section({ title, icon, children }) {
  return (
    <div className="rounded-xl border border-slate-700 bg-slate-950/50 p-4">
      <div className="mb-4 flex items-center gap-2">
        <div className="text-cyan-400">
          {icon}
        </div>

        <h3 className="text-sm font-semibold text-slate-200">
          {title}
        </h3>
      </div>

      {children}
    </div>
  );
}


function InfoRow({ label, value }) {
  return (
    <div className="flex flex-col gap-1 border-b border-slate-800 py-2 last:border-0 sm:flex-row sm:items-center sm:justify-between sm:gap-4">
      <span className="text-xs text-slate-500">
        {label}
      </span>

      <span className="text-sm font-medium text-slate-300">
        {String(value)}
      </span>
    </div>
  );
}


function ListBlock({ title, items }) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div className="mt-3">
      <p className="mb-2 text-xs font-medium text-slate-500">
        {title}
      </p>

      <ul className="space-y-2">
        {items.map((item, index) => (
          <li
            key={index}
            className="flex gap-2 text-sm leading-6 text-slate-400"
          >
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-400" />

            <span>
              {typeof item === "string"
                ? item
                : JSON.stringify(item)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}


/* =========================================================
   HELPERS
========================================================= */

function getAgentNames(agents) {
  if (!agents || typeof agents !== "object") {
    return [
      "Planner Agent",
      "Fish Agent",
      "Ocean Agent",
      "Reasoning Agent",
    ];
  }

  const names = Object.keys(agents);

  if (names.length === 0) {
    return [
      "Planner Agent",
      "Fish Agent",
      "Ocean Agent",
      "Reasoning Agent",
    ];
  }

  return names;
}


function formatAgentName(name) {
  if (!name) {
    return "Agent";
  }

  return String(name)
    .replaceAll("_", " ")
    .replace(/agent/gi, "Agent")
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase()
    );
}
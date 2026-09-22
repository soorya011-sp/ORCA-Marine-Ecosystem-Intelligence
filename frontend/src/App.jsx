import { useState } from "react";
import Login from "./Login";

import {
  Activity,
  AlertTriangle,
  Brain,
  CheckCircle,
  Fish,
  Globe2,
  Map,
  Menu,
  MessageSquare,
  Microscope,
  Navigation,
  Search,
  Shield,
  Waves,
  X,
  Wind,
  CloudRain,
  MapPin,
  Loader2,
  CheckCircle2,
  XCircle,
  Route as RouteIcon,
} from "lucide-react";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
  Polyline,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

const API = "http://127.0.0.1:8000";

const DEFAULT_LAT = 9.5;
const DEFAULT_LON = 76;

const HISTORICAL_DATE = "2020-05-01";

/* =========================================================
   MAIN APP
========================================================= */

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem("orca_logged_in") === "true"
  );

  const [activePage, setActivePage] = useState("dashboard");

  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("orca_logged_in");
    localStorage.removeItem("orca_user");
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }
  const pages = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: Globe2,
    },
    {
      id: "ask",
      label: "Ask ORCA",
      icon: MessageSquare,
    },
    {
      id: "ocean",
      label: "Ocean Analysis",
      icon: Waves,
    },
    {
      id: "pfz",
      label: "PFZ Analysis",
      icon: Fish,
    },
    {
      id: "weather",
      label: "Weather",
      icon: Activity,
    },
    {
      id: "route",
      label: "Safe Route",
      icon: Navigation,
    },
    {
      id: "alerts",
      label: "Alerts",
      icon: AlertTriangle,
    },
    {
      id: "evidence",
      label: "Research Evidence",
      icon: Microscope,
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      <aside
        className={`fixed left-0 top-0 z-50 h-screen border-r border-slate-800 bg-slate-950 transition-all duration-300 ${
          sidebarOpen ? "w-64" : "w-20"
        }`}
      >

        <div className="flex h-20 items-center border-b border-slate-800 px-5">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10">
              <Waves className="h-6 w-6 text-cyan-400" />
            </div>

            {sidebarOpen && (
              <div>
                <h1 className="text-xl font-bold tracking-wide">
                  ORCA
                </h1>

                <p className="text-xs text-slate-500">
                  Marine Intelligence
                </p>
              </div>
            )}

          </div>

        </div>

        <nav className="space-y-2 p-4">

          {pages.map((page) => {

            const Icon = page.icon;
            const active = activePage === page.id;

            return (
              <button
                key={page.id}
                onClick={() => setActivePage(page.id)}
                className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left transition ${
                  active
                    ? "bg-cyan-500/10 text-cyan-400"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white"
                }`}
              >

                <Icon className="h-5 w-5 shrink-0" />

                {sidebarOpen && (
                  <span className="text-sm font-medium">
                    {page.label}
                  </span>
                )}

              </button>
            );
          })}

        </nav>

        {sidebarOpen && (
          <div className="absolute bottom-5 left-4 right-4 rounded-xl border border-slate-800 bg-slate-900 p-4">

            <div className="flex items-center gap-2">

              <div className="h-2 w-2 rounded-full bg-emerald-400" />

              <span className="text-xs text-slate-400">
                ORCA Backend Online
              </span>

            </div>

            <p className="mt-2 text-xs text-slate-600">
  FastAPI • Agentic AI
</p>

<button
  onClick={handleLogout}
  className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg border border-red-500/20 bg-red-500/5 px-3 py-2 text-xs font-medium text-red-400 transition hover:bg-red-500/10 hover:text-red-300"
>
  <XCircle className="h-4 w-4" />
  Logout
</button>

          </div>
        )}

      </aside>

      {/* =====================================================
          MAIN
      ===================================================== */}

      <main
        className={`min-h-screen transition-all duration-300 ${
          sidebarOpen ? "ml-64" : "ml-20"
        }`}
      >

        <header className="sticky top-0 z-40 flex h-20 items-center justify-between border-b border-slate-800 bg-slate-950/90 px-6 backdrop-blur">

          <div className="flex items-center gap-4">

            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="rounded-lg p-2 text-slate-400 hover:bg-slate-900 hover:text-white"
            >

              {sidebarOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}

            </button>

            <div>

              <h2 className="text-lg font-semibold">
                Marine Ecosystem Intelligence
              </h2>

              <p className="text-xs text-slate-500">
                Collaborative AI agents for marine decision support
              </p>

            </div>

          </div>

          <div className="hidden items-center gap-3 md:flex">

            <div className="flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900 px-3 py-2">

              <Globe2 className="h-4 w-4 text-cyan-400" />

              <span className="text-xs text-slate-400">
                Arabian Sea
              </span>

            </div>

            <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/5 px-3 py-2">

              <div className="h-2 w-2 rounded-full bg-emerald-400" />

              <span className="text-xs text-emerald-400">
                System Online
              </span>

            </div>

          </div>

        </header>

        <div className="p-6">

          {activePage === "dashboard" && (
            <Dashboard setActivePage={setActivePage} />
          )}

          {activePage === "ask" && <AskORCA />}

          {activePage === "ocean" && <OceanAnalysis />}

          {activePage === "pfz" && <PFZAnalysis />}

          {activePage === "weather" && <WeatherPage />}

          {activePage === "route" && <SafeRoute />}

          {activePage === "alerts" && <AlertsPage />}

          {activePage === "evidence" && <EvidencePage />}

        </div>

      </main>

    </div>
  );
}

/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard({ setActivePage }) {
  const marineMarkers = [
    { position: [9.9, 75.8], level: "High PFZ" },
    { position: [9.5, 76.0], level: "High PFZ" },
    { position: [9.2, 76.4], level: "Moderate" },
    { position: [9.0, 76.8], level: "Low" },
  ];

  const markerColor = (level) => {
    if (level === "High PFZ") return "#14b8a6";
    if (level === "Moderate") return "#f59e0b";
    return "#ef4444";
  };

  return (
    <div className="mx-auto max-w-7xl space-y-6">

      {/* HERO */}

      <section className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-slate-900 via-slate-950 to-cyan-950/20 p-8">

        <div className="absolute right-0 top-0 h-64 w-64 rounded-full bg-cyan-500/5 blur-3xl" />

        <div className="relative max-w-3xl">

          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/5 px-3 py-1.5 text-xs text-cyan-400">

            <Brain className="h-4 w-4" />

            Agentic Marine Intelligence

          </div>

          <h1 className="text-5xl font-bold tracking-tight">

            Understand the ocean.

            <br />

            <span className="text-cyan-400">
              Act with confidence.
            </span>

          </h1>

          <p className="mt-5 max-w-2xl text-base leading-7 text-slate-400">

            ORCA combines marine observations, weather intelligence,
            fish analysis and collaborative AI agents to transform
            complex ocean data into explainable decisions.

          </p>

          <div className="mt-7 flex flex-wrap gap-3">

            <button
              onClick={() => setActivePage("ask")}
              className="flex items-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400"
            >

              <MessageSquare className="h-5 w-5" />

              Ask ORCA

            </button>

            <button
              onClick={() => setActivePage("pfz")}
              className="flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-900 px-5 py-3 font-semibold text-slate-300 hover:border-cyan-500 hover:text-cyan-400"
            >

              <Map className="h-5 w-5" />

              Explore PFZ

            </button>

          </div>

        </div>

      </section>


      {/* METRICS */}

      <section className="grid gap-4 md:grid-cols-4">

        <MetricCard
          icon={<Waves />}
          title="Marine Intelligence"
          value="ONLINE"
          unit=""
        />

        <MetricCard
          icon={<Fish />}
          title="Fish Analysis"
          value="ACTIVE"
          unit=""
        />

        <MetricCard
          icon={<Activity />}
          title="Weather"
          value="ACTIVE"
          unit=""
        />

        <MetricCard
          icon={<Shield />}
          title="Decision Support"
          value="READY"
          unit=""
          risk
        />

      </section>


      {/* =====================================================
          MARINE ACTIVITY MAP
      ===================================================== */}

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <div className="flex items-center justify-between">

          <div>

            <div className="flex items-center gap-3">

              <MapPin className="h-6 w-6 text-cyan-400" />

              <div>

                <p className="text-xs font-semibold uppercase tracking-[0.15em] text-cyan-400">
                  Marine Activity Map
                </p>

                <h2 className="mt-1 text-2xl font-bold text-white">
                  Marine Region
                </h2>

              </div>

            </div>

            <p className="mt-2 text-sm text-slate-500">
              Environmental activity and potential fishing-zone overview.
            </p>

          </div>

          <button
            onClick={() => setActivePage("pfz")}
            className="rounded-xl border border-slate-700 bg-slate-950 p-3 text-slate-400 transition hover:border-cyan-500 hover:text-cyan-400"
            title="Open full PFZ analysis"
          >

            <Map className="h-5 w-5" />

          </button>

        </div>


        <div className="relative mt-5 overflow-hidden rounded-2xl border border-slate-700">

          <MapContainer
            center={[9.5, 76.0]}
            zoom={7}
            scrollWheelZoom={false}
            className="h-[430px] w-full"
          >

            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {marineMarkers.map((marker, index) => (

              <CircleMarker
                key={index}
                center={marker.position}
                radius={9}
                pathOptions={{
                  color: markerColor(marker.level),
                  fillColor: markerColor(marker.level),
                  fillOpacity: 0.85,
                  weight: 3,
                }}
              >

                <Popup>

                  <div className="text-sm">

                    <strong>Marine Region</strong>

                    <br />

                    Status: {marker.level}

                  </div>

                </Popup>

              </CircleMarker>

            ))}

          </MapContainer>


          {/* REGION LABEL */}

          <div className="absolute left-4 top-4 z-[1000] rounded-xl border border-slate-700 bg-slate-950/90 px-4 py-3 shadow-xl backdrop-blur">

            <div className="flex items-center gap-2">

              <MapPin className="h-4 w-4 text-pink-400" />

              <span className="text-sm font-semibold text-white">
                Marine Region
              </span>

            </div>

          </div>


          {/* LEGEND */}

          <div className="absolute bottom-4 left-4 z-[1000] flex flex-wrap items-center gap-4 rounded-xl border border-slate-700 bg-slate-950/90 px-4 py-3 text-xs backdrop-blur">

            <div className="flex items-center gap-2">

              <span className="h-3 w-3 rounded-full bg-teal-400" />

              <span className="text-slate-300">
                High PFZ
              </span>

            </div>

            <div className="flex items-center gap-2">

              <span className="h-3 w-3 rounded-full bg-amber-400" />

              <span className="text-slate-300">
                Moderate
              </span>

            </div>

            <div className="flex items-center gap-2">

              <span className="h-3 w-3 rounded-full bg-red-400" />

              <span className="text-slate-300">
                Low
              </span>

            </div>

          </div>

        </div>

      </section>


      {/* COLLABORATIVE AI */}

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <SectionTitle
          icon={<Brain />}
          title="Collaborative AI"
        />

        <p className="mt-2 text-sm text-slate-500">

          ORCA coordinates specialized agents instead of relying
          on a single model.

        </p>

        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

          <AgentCard
            icon={<Brain />}
            name="Planner Agent"
            description="Understands intent and decomposes tasks."
          />

          <AgentCard
            icon={<Fish />}
            name="Fish Agent"
            description="Analyzes fish ecosystem indicators."
          />

          <AgentCard
            icon={<Waves />}
            name="Ocean Agent"
            description="Analyzes marine environmental conditions."
          />

          <AgentCard
            icon={<Activity />}
            name="Weather Agent"
            description="Evaluates marine weather conditions."
          />

        </div>

      </section>


      {/* REASONING */}

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <SectionTitle
          icon={<Brain />}
          title="ORCA Reasoning Chain"
        />

        <div className="mt-6 flex flex-wrap items-center gap-3">

          {[
            "User Query",
            "Planner",
            "Marine Data",
            "Specialist Agents",
            "Evidence",
            "Reasoning",
            "Confidence",
            "Decision",
          ].map((item, index) => (

            <div
              key={item}
              className="flex items-center gap-3"
            >

              <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 px-4 py-3 text-sm text-cyan-300">
                {item}
              </div>

              {index < 7 && (
                <span className="text-slate-700">
                  →
                </span>
              )}

            </div>

          ))}

        </div>

      </section>

    </div>
  );
}
/* =========================================================
   ASK ORCA
========================================================= */

function AskORCA() {

  const [question, setQuestion] = useState(
    "Why has fish productivity declined near Kerala?"
  );

  const [selectedDate, setSelectedDate] = useState(
    HISTORICAL_DATE
  );

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const askORCA = async () => {

    const cleanQuestion = question.trim();

    if (!cleanQuestion) {
      setError("Please enter a question for ORCA.");
      return;
    }

    if (!selectedDate) {
      setError("Please select an observation date.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const params = new URLSearchParams({
        query: cleanQuestion,
        species: "Indian Oil Sardine",
        lat: String(DEFAULT_LAT),
        lon: String(DEFAULT_LON),
        date: selectedDate,
        salinity: "34",
      });

      const response = await fetch(
        `${API}/agentic-orca?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();

      setResult(data);

    } catch (err) {

      console.error(err);

      setError(
        "ORCA could not process the request. Check that the FastAPI backend is running on port 8000 and that the requested date has available data."
      );

    } finally {

      setLoading(false);

    }

  };

  return (
    <div className="mx-auto max-w-6xl space-y-6">

      <PageHero
        icon={<Brain />}
        title={
          <>
            Ask <span className="text-cyan-400">ORCA</span>
          </>
        }
        description="Ask complex questions about fish productivity, ocean conditions, marine ecosystems, weather and safety."
      />

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

        <div className="flex items-center gap-2">

          <Search className="h-5 w-5 text-cyan-400" />

          <h2 className="font-semibold">
            Marine Intelligence Query
          </h2>

        </div>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={4}
          className="mt-4 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-sm text-white outline-none focus:border-cyan-500"
          placeholder="Ask ORCA..."
        />

        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">

          <div>

            <label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-500">
              Observation Date
            </label>

            <input
              type="date"
              value={selectedDate}
              max={new Date().toISOString().split("T")[0]}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500"
            />

          </div>

          <div className="flex items-end">

            <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 px-4 py-3">

              <p className="text-[11px] uppercase tracking-wider text-cyan-400">
                Data Mode
              </p>

              <p className="mt-1 text-sm font-semibold text-slate-200">
                Date-specific observation
              </p>

            </div>

          </div>

        </div>

        <div className="mt-4 flex flex-wrap gap-3">

          <QuickQuestion
            text="Fish productivity"
            onClick={() =>
              setQuestion(
                "Why has fish productivity declined near Kerala?"
              )
            }
          />

          <QuickQuestion
            text="Fish ecosystem"
            onClick={() =>
              setQuestion(
                "What environmental conditions may affect Indian Oil Sardine?"
              )
            }
          />

          <QuickQuestion
            text="Ocean conditions"
            onClick={() =>
              setQuestion(
                "Are ocean conditions favorable for Indian Oil Sardine?"
              )
            }
          />

        </div>

        <button
          onClick={askORCA}
          disabled={loading}
          className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
        >

          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              ORCA is reasoning...
            </>
          ) : (
            <>
              <Brain className="h-5 w-5" />
              Ask ORCA
            </>
          )}

        </button>

      </section>

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {loading && <LoadingORCA />}

      {result && !loading && (
        <ORCAResult data={result} />
      )}

    </div>
  );
}

function OceanAnalysis() {

  const [selectedDate, setSelectedDate] = useState(
    HISTORICAL_DATE
  );

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const analyzeOcean = async () => {

    if (!selectedDate) {
      setError("Please select an observation date.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const params = new URLSearchParams({
        lat: String(DEFAULT_LAT),
        lon: String(DEFAULT_LON),
        date: selectedDate,
        salinity: "34",
      });

      const response = await fetch(
        `${API}/ocean-location-analysis?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();

      setResult(data);

    } catch (err) {

      console.error(err);

      setError(
        "Ocean analysis failed. Check that the backend is running and that the requested date has available data."
      );

    } finally {

      setLoading(false);

    }

  };

  const ocean =
    result?.ocean_analysis ||
    result ||
    {};

  const temperature =
    ocean.temperature ??
    ocean.sst ??
    result?.observations?.sea_surface_temperature ??
    null;

  const chlorophyll =
    ocean.chlorophyll ??
    ocean.chl ??
    result?.observations?.chlorophyll ??
    null;

  const salinity =
    ocean.salinity ??
    result?.observations?.salinity ??
    34;

  const condition =
    ocean.ocean_condition ??
    ocean.condition ??
    ocean.status ??
    "N/A";

  return (
    <div className="mx-auto max-w-6xl space-y-6">

      <PageHero
        icon={<Waves />}
        title={
          <>
            Ocean <span className="text-cyan-400">
              Analysis
            </span>
          </>
        }
        description="Analyze sea surface temperature, chlorophyll and marine environmental conditions for a selected observation date."
      />

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <div className="grid gap-4 md:grid-cols-4">

          <InfoBox
            title="Location"
            value="Kerala / Arabian Sea"
          />

          <InfoBox
            title="Coordinates"
            value="9.50° N, 76.00° E"
          />

          <div>

            <label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-500">
              Observation Date
            </label>

            <input
              type="date"
              value={selectedDate}
              max={new Date().toISOString().split("T")[0]}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500"
            />

          </div>

          <InfoBox
            title="Analysis Mode"
            value="Date-specific"
          />

        </div>

        <button
          onClick={analyzeOcean}
          disabled={loading}
          className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
        >

          {loading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Waves className="h-5 w-5" />
          )}

          {loading
            ? "Analyzing ocean..."
            : "Analyze Ocean"}

        </button>

      </section>

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {loading && (
        <LoadingBox
          title="ORCA is analyzing ocean conditions"
          description="Selected date → SST → Chlorophyll → Salinity → Ocean stress"
        />
      )}

      {result && !loading && (
        <>

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

            <div className="flex flex-wrap items-center gap-3 text-sm">

              <span className="text-slate-500">
                Requested observation:
              </span>

              <span className="rounded-full border border-cyan-500/20 bg-cyan-500/5 px-3 py-1 text-cyan-400">
                {selectedDate}
              </span>

              <span className="text-slate-600">
                Historical / source availability determines whether an observation is returned.
              </span>

            </div>

          </section>

          <section className="grid gap-4 md:grid-cols-4">

            <MetricCard
              icon={<Waves />}
              title="Sea Surface Temperature"
              value={formatValue(temperature)}
              unit="°C"
            />

            <MetricCard
              icon={<Activity />}
              title="Chlorophyll"
              value={formatValue(chlorophyll)}
              unit="mg/m³"
            />

            <MetricCard
              icon={<Waves />}
              title="Salinity"
              value={formatValue(salinity)}
              unit="PSU"
            />

            <MetricCard
              icon={<Shield />}
              title="Ocean Condition"
              value={condition}
              unit=""
              risk
            />

          </section>

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<Brain />}
              title="ORCA Ocean Interpretation"
            />

            <div className="mt-5 space-y-3">

              <Interpretation
                title="Sea Surface Temperature"
                value={temperature}
                text={
                  temperature !== null
                    ? temperature > 29
                      ? "Elevated SST detected. This may influence marine habitat suitability."
                      : "No strong elevated-temperature signal detected."
                    : "SST data unavailable for the selected date."
                }
              />

              <Interpretation
                title="Chlorophyll"
                value={chlorophyll}
                text={
                  chlorophyll !== null
                    ? chlorophyll < 0.5
                      ? "Low chlorophyll may indicate reduced primary productivity."
                      : "Chlorophyll does not show a strong low-productivity signal."
                    : "Chlorophyll data unavailable for the selected date."
                }
              />

            </div>

          </section>

        </>
      )}

    </div>
  );
}

function PFZAnalysis() {

  const pfzPoints = [
    {
      lat: 9.5,
      lon: 76.0,
      score: 92,
      label: "High PFZ potential",
    },
    {
      lat: 9.65,
      lon: 76.15,
      score: 84,
      label: "Good PFZ potential",
    },
    {
      lat: 9.35,
      lon: 75.85,
      score: 76,
      label: "Moderate PFZ potential",
    },
    {
      lat: 9.8,
      lon: 76.3,
      score: 68,
      label: "Moderate PFZ potential",
    },
  ];

  return (
    <div className="mx-auto max-w-7xl space-y-6">

      <PageHero
        icon={<Map />}
        title={
          <>
            Potential Fishing{" "}
            <span className="text-cyan-400">
              Zone Analysis
            </span>
          </>
        }
        description="Explore marine environmental conditions and potential fishing zones using an interactive map."
      />

      <section className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">

        <div className="border-b border-slate-800 p-5">

          <div className="flex items-center justify-between">

            <div>

              <h2 className="font-semibold">
                PFZ Spatial Intelligence
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Kerala / Southeastern Arabian Sea
              </p>

            </div>

            <div className="flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/5 px-3 py-1.5">

              <div className="h-2 w-2 rounded-full bg-cyan-400" />

              <span className="text-xs text-cyan-400">
                Spatial Analysis
              </span>

            </div>

          </div>

        </div>

        {/* INCOIS BASELINE VS ORCA AUGMENTATION */}
        <div className="grid grid-cols-1 gap-4 border-b border-slate-800 p-5 md:grid-cols-2">

          <div className="rounded-xl border border-slate-700 bg-slate-800/60 p-4">
            <div className="mb-2 flex items-center justify-between gap-3">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Official INCOIS PFZ Baseline
              </span>
              <span className="rounded bg-blue-500/20 px-2 py-0.5 font-mono text-xs font-semibold text-blue-400">
                INCOIS PFZ
              </span>
            </div>
            <p className="text-sm font-medium text-slate-200">
              Sector: Kerala / Kochi Offshore (9.5°N, 76.0°E)
            </p>
            <p className="mt-1 text-xs text-slate-400">
              Status: Active Potential Fishing Zone (PFZ) baseline
            </p>
            <p className="mt-2 text-xs leading-5 text-slate-500">
              ORCA uses this advisory as a baseline and adds species, environmental, safety and evidence context.
            </p>
          </div>

          <div className="rounded-xl border border-cyan-500/30 bg-cyan-950/20 p-4">
            <div className="mb-2 flex items-center justify-between gap-3">
              <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                ORCA Explainable Augmentation
              </span>
              <span className="rounded bg-cyan-500/20 px-2 py-0.5 font-mono text-xs font-bold text-cyan-300">
                Augmented Layer
              </span>
            </div>
            <p className="text-sm font-medium text-slate-200">
              Advisory: Consider a deeper sector (sardine thermal-stress signal)
            </p>
            <div className="mt-2 space-y-1 text-xs leading-5">
              <p className="text-slate-300">
                • <strong className="text-cyan-400">Biological Suitability:</strong> SST 31.85°C is above the 26–29°C range reported for Indian oil sardine aggregation conditions in the reference study.
              </p>
              <p className="text-slate-300">
                • <strong className="text-emerald-400">Vessel Safety Context:</strong> Wave height 1.2 m is evaluated against the selected vessel-class threshold in Safe Route.
              </p>
              <p className="text-slate-300">
                • <strong className="text-amber-400">Epistemic Confidence:</strong> 56% prototype assessment confidence with limited environmental indicators.
              </p>
            </div>
          </div>

        </div>

        <div className="h-[520px]">

          <MapContainer
            center={[9.5, 76]}
            zoom={7}
            scrollWheelZoom={true}
            className="h-full w-full"
          >

            <TileLayer
              attribution="&copy; OpenStreetMap contributors"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {pfzPoints.map((point, index) => (

              <CircleMarker
                key={index}
                center={[
                  point.lat,
                  point.lon,
                ]}
                radius={
                  point.score > 85
                    ? 16
                    : 12
                }
                pathOptions={{
                  color:
                    point.score > 85
                      ? "#22d3ee"
                      : "#38bdf8",
                  fillColor:
                    point.score > 85
                      ? "#06b6d4"
                      : "#0ea5e9",
                  fillOpacity: 0.55,
                  weight: 2,
                }}
              >

                <Popup>

                  <div className="text-sm">

                    <strong>
                      {point.label}
                    </strong>

                    <br />

                    PFZ Score:{" "}
                    <strong>
                      {point.score}
                    </strong>

                    <br />

                    Lat: {point.lat}

                    <br />

                    Lon: {point.lon}

                  </div>

                </Popup>

              </CircleMarker>

            ))}

          </MapContainer>

        </div>

      </section>

      <section className="grid gap-4 md:grid-cols-3">

        <MetricCard
          icon={<Fish />}
          title="Best PFZ Score"
          value="92"
          unit=""
        />

        <MetricCard
          icon={<Map />}
          title="PFZ Candidates"
          value="4"
          unit="zones"
        />

        <MetricCard
          icon={<Brain />}
          title="Analysis Mode"
          value="Spatial"
          unit=""
        />

      </section>

    </div>
  );
}

/* =========================================================
   WEATHER
========================================================= */

function WeatherPage() {

  const [region, setRegion] = useState("Kerala / Arabian Sea");
  const [latitude, setLatitude] = useState(String(DEFAULT_LAT));
  const [longitude, setLongitude] = useState(String(DEFAULT_LON));

  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeWeather = async () => {

    setError("");
    setWeather(null);

    const lat = Number(latitude);
    const lon = Number(longitude);

    if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
      setError("Please enter valid latitude and longitude values.");
      return;
    }

    if (lat < -90 || lat > 90) {
      setError("Latitude must be between -90 and 90.");
      return;
    }

    if (lon < -180 || lon > 180) {
      setError("Longitude must be between -180 and 180.");
      return;
    }

    setLoading(true);

    try {

      const params = new URLSearchParams({
        lat: String(lat),
        lon: String(lon),
      });

      const response = await fetch(
        `${API}/weather-location-analysis?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();

      setWeather(data);

    } catch (err) {

      console.error(err);

      setError(
        "Weather analysis could not be loaded. Check that the FastAPI backend is running on port 8000."
      );

    } finally {

      setLoading(false);

    }

  };

  const source =
    weather?.weather ||
    weather?.data?.weather ||
    weather?.data ||
    weather ||
    {};

  const analysis =
    weather?.analysis ||
    weather?.weather_analysis ||
    weather?.route_analysis ||
    weather?.data?.analysis ||
    {};

  const marineConditions =
    analysis?.marine_conditions ||
    weather?.marine_conditions ||
    {};

  const safetyData =
    analysis?.safety ||
    weather?.safety ||
    {};

  const windSpeed =
    source?.wind_speed ??
    source?.windSpeed ??
    marineConditions?.wind_speed ??
    analysis?.wind_speed ??
    null;

  const rainfall =
    source?.rainfall ??
    source?.precipitation ??
    marineConditions?.rainfall ??
    analysis?.rainfall ??
    null;

  const waveHeight =
    source?.wave_height ??
    source?.waveHeight ??
    marineConditions?.wave_height ??
    analysis?.wave_height ??
    null;

  const condition =
    source?.weather_condition ??
    source?.weatherCondition ??
    marineConditions?.weather_condition ??
    analysis?.weather_condition ??
    source?.condition ??
    "Unknown";

  const safetyRisk =
    source?.safety_risk ??
    source?.safetyRisk ??
    analysis?.safety_risk ??
    analysis?.risk_level ??
    safetyData?.safety ??
    (
      windSpeed !== null || waveHeight !== null
        ? (
            Number(windSpeed) > 30 || Number(waveHeight) > 2.5
              ? "High"
              : Number(windSpeed) > 15 || Number(waveHeight) > 1.5
                ? "Moderate"
                : "Low"
          )
        : "Unknown"
    );

  return (
    <div className="mx-auto max-w-6xl space-y-6">

      <PageHero
        icon={<Activity />}
        title={
          <>
            Weather{" "}
            <span className="text-cyan-400">
              Intelligence
            </span>
          </>
        }
        description="Analyze wind, rainfall, waves and marine weather conditions for fishing and navigation."
      />

      {/* LOCATION INPUT */}

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <div className="grid gap-4 md:grid-cols-3">

          {/* REGION */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Region
            </label>

            <input
              type="text"
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              placeholder="Enter marine region"
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10"
            />
          </div>

          {/* LATITUDE */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Latitude
            </label>

            <input
              type="number"
              step="0.01"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              placeholder="9.50"
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10"
            />
          </div>

          {/* LONGITUDE */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Longitude
            </label>

            <input
              type="number"
              step="0.01"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              placeholder="76.00"
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10"
            />
          </div>

        </div>

        <button
          onClick={analyzeWeather}
          disabled={loading}
          className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
        >

          {loading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Activity className="h-5 w-5" />
          )}

          {loading
            ? "ORCA is analyzing weather..."
            : "Analyze Weather"}

        </button>

      </section>

      {/* LOCATION SUMMARY */}

      {weather && !loading && (
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

          <div className="flex flex-wrap items-center gap-4 text-sm">

            <div>
              <span className="text-slate-500">
                Region
              </span>

              <span className="ml-2 font-medium text-cyan-400">
                {region || "Marine Region"}
              </span>
            </div>

            <div>
              <span className="text-slate-500">
                Latitude
              </span>

              <span className="ml-2 font-medium text-white">
                {Number(latitude).toFixed(2)}° N
              </span>
            </div>

            <div>
              <span className="text-slate-500">
                Longitude
              </span>

              <span className="ml-2 font-medium text-white">
                {Number(longitude).toFixed(2)}° E
              </span>
            </div>

          </div>

        </section>
      )}

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {loading && (
        <LoadingBox
          title="ORCA is analyzing marine weather"
          description="Wind → Rainfall → Waves → Safety"
        />
      )}

      {weather && !loading && (

        <div className="space-y-6">

          <section className="grid gap-4 md:grid-cols-4">

            <MetricCard
              icon={<Wind />}
              title="Wind Speed"
              value={formatValue(windSpeed)}
              unit="km/h"
            />

            <MetricCard
              icon={<Waves />}
              title="Wave Height"
              value={formatValue(waveHeight)}
              unit="m"
            />

            <MetricCard
              icon={<CloudRain />}
              title="Rainfall"
              value={formatValue(rainfall)}
              unit="mm"
            />

            <MetricCard
              icon={<Shield />}
              title="Safety Risk"
              value={safetyRisk}
              unit=""
              risk
            />

          </section>

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<Waves />}
              title="Current Marine Conditions"
            />

            <div className="mt-5 grid gap-4 md:grid-cols-2">

              <div className="rounded-xl bg-slate-950 p-5">

                <p className="text-xs uppercase tracking-wider text-slate-500">
                  Weather Condition
                </p>

                <p className="mt-2 text-2xl font-bold text-cyan-400">
                  {condition}
                </p>

              </div>

              <div className="rounded-xl bg-slate-950 p-5">

                <p className="text-xs uppercase tracking-wider text-slate-500">
                  Marine Safety
                </p>

                <div className="mt-3">
                  <RiskBadge risk={safetyRisk} />
                </div>

              </div>

            </div>

          </section>

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<Brain />}
              title="ORCA Weather Interpretation"
            />

            <div className="mt-5 space-y-3">

              <Interpretation
                title="Wind"
                value={windSpeed}
                text={
                  windSpeed !== null
                    ? windSpeed > 30
                      ? "Strong winds may create difficult marine conditions."
                      : windSpeed > 15
                      ? "Moderate winds are present and should be monitored."
                      : "Wind conditions appear relatively calm."
                    : "Wind data unavailable."
                }
              />

              <Interpretation
                title="Rainfall"
                value={rainfall}
                text={
                  rainfall !== null
                    ? rainfall > 10
                      ? "Significant rainfall may reduce visibility and affect fishing operations."
                      : rainfall > 0
                      ? "Some rainfall is present."
                      : "No significant rainfall detected."
                    : "Rainfall data unavailable."
                }
              />

              <Interpretation
                title="Wave Height"
                value={waveHeight}
                text={
                  waveHeight !== null
                    ? waveHeight > 2.5
                      ? "Higher waves may increase navigation risk."
                      : waveHeight > 1.5
                      ? "Moderate wave conditions are present."
                      : "Wave conditions appear relatively calm."
                    : "Wave data unavailable."
                }
              />

            </div>

          </section>

        </div>

      )}

    </div>
  );
}
/* =========================================================
   SAFE ROUTE
========================================================= */

function SafeRoute() {

  const [startLat, setStartLat] = useState("9.5");
  const [startLon, setStartLon] = useState("76.0");

  const [endLat, setEndLat] = useState("9.8");
  const [endLon, setEndLon] = useState("76.3");

  const [vesselClass, setVesselClass] = useState("motorized");

  const vesselOptions = {
    motorized: {
      label: "Traditional Motorized Craft (OBM)",
      threshold: 1.5,
    },
    trawler: {
      label: "Mechanized Trawler",
      threshold: 2.5,
    },
    deepsea: {
      label: "Deep Sea Fishing Vessel",
      threshold: 3.5,
    },
  };

  const selectedVessel = vesselOptions[vesselClass];

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeRoute = async () => {

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const params = new URLSearchParams({
        start_lat: String(startLat),
        start_lon: String(startLon),
        end_lat: String(endLat),
        end_lon: String(endLon),
        vessel_class: selectedVessel.label,
      });

      const response = await fetch(
        `${API}/route-analysis?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();

      setResult(data);

    } catch (err) {

      console.error(err);

      setError(
        "Safe Route analysis failed. Make sure the FastAPI backend is running on port 8000 and the /route-analysis endpoint is available."
      );

    } finally {

      setLoading(false);

    }

  };

  const routePoints =
    result?.route_analysis?.route_points ||
    result?.route_points ||
    result?.route ||
    result?.points ||
    [];

  const normalizedPoints =
    Array.isArray(routePoints)
      ? routePoints
          .map((point) => {

            if (
              Array.isArray(point) &&
              point.length >= 2
            ) {

              return [
                Number(point[0]),
                Number(point[1]),
              ];

            }

            if (
              point &&
              typeof point === "object"
            ) {

              const lat =
                point.lat ??
                point.latitude;

              const lon =
                point.lon ??
                point.lng ??
                point.longitude;

              if (
                lat !== undefined &&
                lon !== undefined
              ) {

                return [
                  Number(lat),
                  Number(lon),
                ];

              }

            }

            return null;

          })
          .filter(
            (point) =>
              point &&
              Number.isFinite(point[0]) &&
              Number.isFinite(point[1])
          )
      : [];

 const routeData = result?.route_analysis || {};
const weatherData = result?.weather || {};
const safetyData = routeData?.safety || {};
const alertsData = result?.alerts || {};

const weatherCondition =
  weatherData?.weather_condition ??
  routeData?.marine_conditions?.weather_condition ??
  "Unknown";

const windSpeed =
  weatherData?.wind_speed ??
  routeData?.marine_conditions?.wind_speed ??
  null;

const waveHeight =
  weatherData?.wave_height ??
  routeData?.marine_conditions?.wave_height ??
  null;

const weatherRisk =
  safetyData?.safety === "Caution"
    ? "Moderate"
    : safetyData?.safety === "Unsafe"
      ? "High"
      : safetyData?.safety === "Safe"
        ? "Low"
        : waveHeight !== null
          ? Number(waveHeight) > selectedVessel.threshold
            ? "High"
            : Number(waveHeight) > selectedVessel.threshold * 0.75
              ? "Moderate"
              : "Low"
          : "Unknown";

const routeRisk =
  safetyData?.safety === "Caution"
    ? "Moderate"
    : safetyData?.safety === "Unsafe"
      ? "High"
      : alertsData?.overall_level === "Low"
        ? "Low"
        : weatherRisk;

const isSafe =
  routeRisk !== "High" &&
  waveHeight !== null &&
  Number(waveHeight) <= selectedVessel.threshold;

const geofenceStatus =
  result?.geofence_status ??
  result?.geofence_analysis?.status ??
  "Not evaluated";

const oceanCondition =
  result?.ocean_condition ??
  result?.ocean_analysis?.ocean_condition ??
  "Unknown";

const reasoning =
  routeData?.recommendation ??
  result?.reasoning ??
  result?.explanation ??
  "ORCA evaluated the route using available marine conditions.";


  return (
    <div className="mx-auto max-w-7xl space-y-6">

      <PageHero
        icon={<Navigation />}
        title={
          <>
            Safe <span className="text-cyan-400">
              Route
            </span>
          </>
        }
        description="Evaluate marine routes using weather, waves, ocean conditions and route safety indicators."
      />

      {/* ROUTE INPUT */}

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <div className="mb-6 flex items-center gap-2">

          <RouteIcon className="h-5 w-5 text-cyan-400" />

          <h2 className="font-semibold">
            Route Planning
          </h2>

        </div>

        <div className="grid gap-6 lg:grid-cols-2">

          {/* START */}

          <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">

            <div className="mb-5 flex items-center gap-2">

              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">

                <MapPin className="h-5 w-5 text-emerald-400" />

              </div>

              <div>

                <h3 className="font-semibold">
                  Starting Point
                </h3>

                <p className="text-xs text-slate-500">
                  Route origin
                </p>

              </div>

            </div>

            <div className="grid grid-cols-2 gap-4">

              <div>

                <label className="text-xs text-slate-500">
                  Latitude
                </label>

                <input
                  type="number"
                  step="0.01"
                  value={startLat}
                  onChange={(e) =>
                    setStartLat(e.target.value)
                  }
                  className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none focus:border-cyan-500"
                />

              </div>

              <div>

                <label className="text-xs text-slate-500">
                  Longitude
                </label>

                <input
                  type="number"
                  step="0.01"
                  value={startLon}
                  onChange={(e) =>
                    setStartLon(e.target.value)
                  }
                  className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none focus:border-cyan-500"
                />

              </div>

            </div>

          </div>

          {/* DESTINATION */}

          <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">

            <div className="mb-5 flex items-center gap-2">

              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-red-500/10">

                <MapPin className="h-5 w-5 text-red-400" />

              </div>

              <div>

                <h3 className="font-semibold">
                  Destination
                </h3>

                <p className="text-xs text-slate-500">
                  Route destination
                </p>

              </div>

            </div>

            <div className="grid grid-cols-2 gap-4">

              <div>

                <label className="text-xs text-slate-500">
                  Latitude
                </label>

                <input
                  type="number"
                  step="0.01"
                  value={endLat}
                  onChange={(e) =>
                    setEndLat(e.target.value)
                  }
                  className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none focus:border-cyan-500"
                />

              </div>

              <div>

                <label className="text-xs text-slate-500">
                  Longitude
                </label>

                <input
                  type="number"
                  step="0.01"
                  value={endLon}
                  onChange={(e) =>
                    setEndLon(e.target.value)
                  }
                  className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none focus:border-cyan-500"
                />

              </div>

            </div>

          </div>

        </div>

        {/* VESSEL CLASS SELECTOR */}
        <div className="mt-6 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4">
          <div className="grid gap-4 md:grid-cols-[1fr_auto] md:items-end">
            <div className="flex flex-col gap-1">
              <label className="text-xs font-medium text-slate-400">
                Select Vessel Class
              </label>
              <select
                value={vesselClass}
                onChange={(e) => setVesselClass(e.target.value)}
                className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 outline-none focus:border-cyan-500"
              >
                <option value="motorized">Traditional Motorized Craft (OBM) — prototype max wave 1.5 m</option>
                <option value="trawler">Mechanized Trawler — prototype max wave 2.5 m</option>
                <option value="deepsea">Deep Sea Fishing Vessel — prototype max wave 3.5 m</option>
              </select>
            </div>

            <div className="rounded-lg border border-slate-700 bg-slate-950 px-4 py-2">
              <p className="text-[11px] uppercase tracking-wider text-slate-500">
                Selected vessel threshold
              </p>
              <p className="mt-1 text-sm font-semibold text-cyan-400">
                {selectedVessel.label} · {selectedVessel.threshold.toFixed(1)} m
              </p>
            </div>
          </div>
          <p className="mt-2 text-xs leading-5 text-slate-500">
            Prototype vessel-class thresholds for ORCA demonstration; they are not official maritime safety limits.
          </p>
        </div>

        <button
          onClick={analyzeRoute}
          disabled={loading}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
        >

          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              ORCA is analyzing the route...
            </>
          ) : (
            <>
              <Navigation className="h-5 w-5" />
              Analyze Safe Route
            </>
          )}

        </button>

      </section>

      {error && (
        <section className="rounded-xl border border-red-500/20 bg-red-500/5 p-5">

          <div className="flex items-start gap-3">

            <AlertTriangle className="mt-0.5 h-5 w-5 text-red-400" />

            <div>

              <h3 className="font-semibold text-red-400">
                Route Analysis Failed
              </h3>

              <p className="mt-1 text-sm text-red-300/80">
                {error}
              </p>

            </div>

          </div>

        </section>
      )}

      {loading && (
        <LoadingBox
          title="ORCA is analyzing route safety"
          description="Route → Weather → Ocean → Geofence → Risk"
        />
      )}

      {result && !loading && (

        <div className="space-y-6">

          {/* STATUS */}

          <section className="grid gap-4 md:grid-cols-5">

            <MetricCard
              icon={
                isSafe
                  ? <CheckCircle2 />
                  : <XCircle />
              }
              title="Route Status"
              value={
                isSafe
                  ? "SAFE"
                  : "RISK"
              }
              unit=""
              risk={!isSafe}
            />

            <MetricCard
              icon={<Wind />}
              title="Weather Risk"
              value={formatValue(weatherRisk)}
              unit=""
              risk
            />

            <MetricCard
              icon={<CloudRain />}
              title="Weather"
              value={formatValue(weatherCondition)}
              unit=""
            />

            <MetricCard
              icon={<Shield />}
              title="Geofence"
              value={formatValue(geofenceStatus)}
              unit=""
              risk
            />

            <MetricCard
              icon={<Waves />}
              title="Ocean Condition"
              value={formatValue(oceanCondition)}
              unit=""
              risk
            />

          </section>

          {/* MAP */}

          <section className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">

            <div className="border-b border-slate-800 p-5">

              <div className="flex items-center justify-between">

                <div>

                  <div className="flex items-center gap-2">

                    <Navigation className="h-5 w-5 text-cyan-400" />

                    <h2 className="font-semibold">
                      Marine Route Map
                    </h2>

                  </div>

                  <p className="mt-1 text-xs text-slate-500">
                    {startLat}°, {startLon}° → {endLat}°, {endLon}°
                  </p>

                </div>

                <div className="rounded-full border border-cyan-500/20 bg-cyan-500/5 px-3 py-1.5">

                  <span className="text-xs text-cyan-400">
                    ORCA Route Analysis
                  </span>

                </div>

              </div>

            </div>

            <div className="h-[520px]">

              <MapContainer
                center={[
                  (
                    Number(startLat) +
                    Number(endLat)
                  ) / 2,

                  (
                    Number(startLon) +
                    Number(endLon)
                  ) / 2,
                ]}
                zoom={8}
                scrollWheelZoom={true}
                className="h-full w-full"
              >

                <TileLayer
                  attribution="&copy; OpenStreetMap contributors"
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                <CircleMarker
                  center={[
                    Number(startLat),
                    Number(startLon),
                  ]}
                  radius={10}
                  pathOptions={{
                    color: "#34d399",
                    fillColor: "#10b981",
                    fillOpacity: 0.8,
                    weight: 3,
                  }}
                >

                  <Popup>
                    <strong>
                      Starting Point
                    </strong>

                    <br />

                    Lat: {startLat}

                    <br />

                    Lon: {startLon}
                  </Popup>

                </CircleMarker>

                <CircleMarker
                  center={[
                    Number(endLat),
                    Number(endLon),
                  ]}
                  radius={10}
                  pathOptions={{
                    color: "#f87171",
                    fillColor: "#ef4444",
                    fillOpacity: 0.8,
                    weight: 3,
                  }}
                >

                  <Popup>
                    <strong>
                      Destination
                    </strong>

                    <br />

                    Lat: {endLat}

                    <br />

                    Lon: {endLon}
                  </Popup>

                </CircleMarker>

                {normalizedPoints.length >= 2 && (

                  <Polyline
                    positions={normalizedPoints}
                    pathOptions={{
                      color: isSafe
                        ? "#22d3ee"
                        : "#f59e0b",
                      weight: 5,
                      opacity: 0.85,
                    }}
                  />

                )}

                {normalizedPoints.length < 2 && (

                  <Polyline
                    positions={[
                      [
                        Number(startLat),
                        Number(startLon),
                      ],
                      [
                        Number(endLat),
                        Number(endLon),
                      ],
                    ]}
                    pathOptions={{
                      color: "#22d3ee",
                      weight: 5,
                      opacity: 0.75,
                      dashArray: "10 8",
                    }}
                  />

                )}

              </MapContainer>

            </div>

          </section>

          {/* CONDITIONS */}

          <section className="grid gap-4 md:grid-cols-4">

            <MetricCard
              icon={<Navigation />}
              title="Vessel Class"
              value={selectedVessel.label}
              unit=""
            />

            <MetricCard
              icon={<Wind />}
              title="Wind Speed"
              value={formatValue(windSpeed)}
              unit={
                windSpeed !== null
                  ? "km/h"
                  : ""
              }
            />

            <MetricCard
              icon={<Waves />}
              title="Wave Height"
              value={formatValue(waveHeight)}
              unit={
                waveHeight !== null
                  ? "m"
                  : ""
              }
            />

            <MetricCard
              icon={<Shield />}
              title="Route Risk"
              value={formatValue(routeRisk)}
              unit=""
              risk
            />

          </section>

          {/* REASONING */}

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<Brain />}
              title="ORCA Route Reasoning"
            />

            <div className="mt-5 space-y-3">

              {Array.isArray(reasoning) ? (

                reasoning.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="flex gap-3 rounded-xl bg-slate-950 p-4"
                    >

                      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs font-bold text-cyan-400">
                        {index + 1}
                      </div>

                      <p className="text-sm leading-6 text-slate-300">
                        {String(item)}
                      </p>

                    </div>

                  )
                )

              ) : reasoning ? (

                <div className="rounded-xl bg-slate-950 p-5">

                  <p className="text-sm leading-6 text-slate-300">
                    {String(reasoning)}
                  </p>

                </div>

              ) : (

                <div className="rounded-xl bg-slate-950 p-5">

                  <p className="text-sm leading-6 text-slate-400">
                    ORCA evaluated the available route,
                    weather and environmental indicators.
                  </p>

                </div>

              )}

            </div>

          </section>

          {/* FINAL DECISION */}

          <section
            className={`rounded-2xl border p-6 ${
              isSafe
                ? "border-emerald-500/20 bg-emerald-500/5"
                : "border-amber-500/20 bg-amber-500/5"
            }`}
          >

            <div className="flex gap-4">

              <div
                className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl ${
                  isSafe
                    ? "bg-emerald-500/10"
                    : "bg-amber-500/10"
                }`}
              >

                {isSafe ? (
                  <CheckCircle2 className="h-6 w-6 text-emerald-400" />
                ) : (
                  <AlertTriangle className="h-6 w-6 text-amber-400" />
                )}

              </div>

              <div>

                <p
                  className={`text-xs font-semibold uppercase tracking-wider ${
                    isSafe
                      ? "text-emerald-400"
                      : "text-amber-400"
                  }`}
                >
                  ORCA Route Decision
                </p>

                <h2 className="mt-2 text-xl font-semibold">

                  {isSafe
                    ? "Route appears suitable based on available indicators."
                    : "Route requires caution based on available indicators."}

                </h2>

                <p className="mt-3 text-sm leading-6 text-slate-400">

                  ORCA's route assessment is based on
                  available environmental and safety
                  indicators. It should not replace official
                  maritime navigation or safety advisories.

                </p>

              </div>

            </div>

          </section>

        </div>

      )}

    </div>
  );
}

/* =========================================================
   ALERTS
========================================================= */

function AlertsPage() {

  const [query, setQuery] = useState(
    "Are there any marine safety alerts for fishing?"
  );

  const [alerts, setAlerts] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeAlerts = async () => {

    const cleanQuery = query.trim();

    if (!cleanQuery) return;

    setLoading(true);
    setError("");
    setAlerts(null);

    try {

      const params = new URLSearchParams({
        query: cleanQuery,
        lat: String(DEFAULT_LAT),
        lon: String(DEFAULT_LON),
      });

      const response = await fetch(
        `${API}/alerts?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();

      console.log("Alerts API:", data);

      setAlerts(data);

    } catch (err) {

      console.error("Alerts error:", err);

      setError(
        "Marine alert analysis failed. Check that the FastAPI backend is running on port 8000 and the /alerts endpoint is available."
      );

    } finally {

      setLoading(false);

    }

  };

  const analysis =
    alerts?.alert_analysis ||
    alerts?.analysis ||
    {};

  const alertList =
    alerts?.alerts ||
    alerts?.data?.alerts ||
    analysis?.alerts ||
    [];

  const alertWeather =
    alerts?.weather ||
    alerts?.data?.weather ||
    analysis?.weather ||
    {};

  const routeAnalysis =
    alerts?.route_analysis ||
    analysis?.route_analysis ||
    {};

  const marineConditions =
    routeAnalysis?.marine_conditions ||
    analysis?.marine_conditions ||
    alerts?.marine_conditions ||
    {};

  const safetyData =
    routeAnalysis?.safety ||
    analysis?.safety ||
    alerts?.safety ||
    {};

  const overallLevel =
    alerts?.overall_level ??
    analysis?.overall_level ??
    alerts?.alert_level ??
    alerts?.risk_level ??
    safetyData?.safety ??
    "Unknown";

  const scientificNote =
    alerts?.scientific_note ||
    analysis?.scientific_note ||
    "ORCA evaluates available marine weather and environmental indicators to identify potential safety concerns.";

  const windSpeed =
    alerts?.wind_speed ??
    alertWeather?.wind_speed ??
    marineConditions?.wind_speed ??
    analysis?.wind_speed ??
    null;

  const waveHeight =
    alerts?.wave_height ??
    alertWeather?.wave_height ??
    marineConditions?.wave_height ??
    analysis?.wave_height ??
    null;

  const rainfall =
    alerts?.rainfall ??
    alertWeather?.rainfall ??
    marineConditions?.rainfall ??
    analysis?.rainfall ??
    null;

  const weatherCondition =
    alerts?.weather_condition ??
    alertWeather?.weather_condition ??
    marineConditions?.weather_condition ??
    analysis?.weather_condition ??
    "Unknown";

  return (
    <div className="mx-auto max-w-7xl space-y-6">

      <PageHero
        icon={<AlertTriangle />}
        title={
          <>
            Marine{" "}
            <span className="text-cyan-400">
              Alerts
            </span>
          </>
        }
        description="Monitor marine weather conditions and identify potential hazards before fishing or navigation."
      />

      {/* QUERY */}

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10">

            <Shield className="h-5 w-5 text-cyan-400" />

          </div>

          <div>

            <h2 className="font-semibold">
              Marine Safety Monitoring
            </h2>

            <p className="text-xs text-slate-500">
              ORCA evaluates available marine conditions
            </p>

          </div>

        </div>

        <textarea
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
          rows={3}
          className="mt-5 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-sm text-white outline-none focus:border-cyan-500"
          placeholder="Ask ORCA about marine alerts..."
        />

        <div className="mt-4 flex flex-wrap gap-2">

          <QuickQuestion
            text="Fishing safety"
            onClick={() =>
              setQuery(
                "Are there any marine safety alerts for fishing?"
              )
            }
          />

          <QuickQuestion
            text="Strong winds"
            onClick={() =>
              setQuery(
                "Are strong winds creating a marine safety risk?"
              )
            }
          />

          <QuickQuestion
            text="Wave conditions"
            onClick={() =>
              setQuery(
                "Are wave conditions safe for fishing?"
              )
            }
          />

          <QuickQuestion
            text="Rainfall"
            onClick={() =>
              setQuery(
                "Is rainfall creating any marine safety concern?"
              )
            }
          />

        </div>

        <button
          onClick={analyzeAlerts}
          disabled={loading}
          className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
        >

          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              ORCA is analyzing alerts...
            </>
          ) : (
            <>
              <AlertTriangle className="h-5 w-5" />
              Analyze Marine Alerts
            </>
          )}

        </button>

      </section>

      {/* ERROR */}

      {error && (
        <section className="rounded-2xl border border-red-500/20 bg-red-500/5 p-5">

          <div className="flex items-start gap-3">

            <AlertTriangle className="mt-0.5 h-5 w-5 text-red-400" />

            <div>

              <h3 className="font-semibold text-red-400">
                Alert Analysis Failed
              </h3>

              <p className="mt-1 text-sm leading-6 text-red-300/80">
                {error}
              </p>

            </div>

          </div>

        </section>
      )}

      {loading && (
        <LoadingBox
          title="ORCA is monitoring marine hazards"
          description="Weather → Waves → Rainfall → Safety → Alerts"
        />
      )}

      {alerts && !loading && (

        <div className="space-y-6">

          {/* LOCATION */}

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<MapPin />}
              title="Monitoring Location"
            />

            <div className="mt-5 grid gap-4 md:grid-cols-4">

              <InfoBox
                title="Region"
                value="Kerala / Arabian Sea"
              />

              <InfoBox
                title="Latitude"
                value={`${DEFAULT_LAT.toFixed(2)}° N`}
              />

              <InfoBox
                title="Longitude"
                value={`${DEFAULT_LON.toFixed(2)}° E`}
              />

              <InfoBox
                title="Weather"
                value={weatherCondition}
              />

            </div>

          </section>

          {/* OVERALL ALERT */}

          <section
            className={`rounded-2xl border p-6 ${
              String(overallLevel)
                .toLowerCase()
                .includes("high")
                ? "border-red-500/30 bg-red-500/5"
                : String(overallLevel)
                    .toLowerCase()
                    .includes("moderate")
                ? "border-amber-500/30 bg-amber-500/5"
                : "border-emerald-500/30 bg-emerald-500/5"
            }`}
          >

            <div className="flex items-start gap-4">

              <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-slate-950">

                {String(overallLevel)
                  .toLowerCase()
                  .includes("high") ? (
                  <AlertTriangle className="h-7 w-7 text-red-400" />
                ) : String(overallLevel)
                    .toLowerCase()
                    .includes("moderate") ? (
                  <AlertTriangle className="h-7 w-7 text-amber-400" />
                ) : (
                  <CheckCircle2 className="h-7 w-7 text-emerald-400" />
                )}

              </div>

              <div className="flex-1">

                <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                  ORCA Alert Assessment
                </p>

                <div className="mt-2 flex flex-wrap items-center gap-3">

                  <h2 className="text-2xl font-bold">
                    {overallLevel}
                  </h2>

                  <RiskBadge
                    risk={overallLevel}
                  />

                </div>

                <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400">

                  ORCA evaluated the available marine weather
                  indicators and identified potential safety
                  conditions relevant to the requested activity.

                </p>

              </div>

            </div>

          </section>

          {/* WEATHER METRICS */}

          <section className="grid gap-4 md:grid-cols-4">

            <MetricCard
              icon={<Wind />}
              title="Wind Speed"
              value={formatValue(windSpeed)}
              unit={
                windSpeed !== null
                  ? "km/h"
                  : ""
              }
            />

            <MetricCard
              icon={<Waves />}
              title="Wave Height"
              value={formatValue(waveHeight)}
              unit={
                waveHeight !== null
                  ? "m"
                  : ""
              }
            />

            <MetricCard
              icon={<CloudRain />}
              title="Rainfall"
              value={formatValue(rainfall)}
              unit={
                rainfall !== null
                  ? "mm"
                  : ""
              }
            />

            <MetricCard
              icon={<Shield />}
              title="Alert Level"
              value={formatValue(overallLevel)}
              unit=""
              risk
            />

          </section>

          {/* ALERT LIST */}

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<AlertTriangle />}
              title="Detected Marine Alerts"
            />

            {Array.isArray(alertList) &&
            alertList.length > 0 ? (

              <div className="mt-5 space-y-4">

                {alertList.map(
                  (alert, index) => {

                    const message =
                      typeof alert === "string"
                        ? alert
                        : alert?.message ||
                          alert?.description ||
                          alert?.alert ||
                          alert?.reason ||
                          "Marine condition requires attention.";

                    const level =
                      typeof alert === "object"
                        ? alert?.level ||
                          alert?.severity ||
                          alert?.risk ||
                          "Warning"
                        : "Warning";

                    return (
                      <div
                        key={index}
                        className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                      >

                        <div className="flex items-start gap-4">

                          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-amber-500/10">

                            <AlertTriangle className="h-5 w-5 text-amber-400" />

                          </div>

                          <div className="flex-1">

                            <div className="flex flex-wrap items-center justify-between gap-3">

                              <h3 className="font-semibold text-slate-200">
                                Marine Safety Alert
                              </h3>

                              <RiskBadge
                                risk={level}
                              />

                            </div>

                            <p className="mt-3 text-sm leading-6 text-slate-400">
                              {String(message)}
                            </p>

                          </div>

                        </div>

                      </div>
                    );
                  }
                )}

              </div>

            ) : (

              <div className="mt-5 rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-6">

                <div className="flex items-center gap-3">

                  <CheckCircle2 className="h-6 w-6 text-emerald-400" />

                  <div>

                    <h3 className="font-semibold text-emerald-400">
                      No major alerts detected
                    </h3>

                    <p className="mt-1 text-sm text-slate-400">
                      ORCA did not identify a significant alert
                      from the available indicators.
                    </p>

                  </div>

                </div>

              </div>

            )}

          </section>

          {/* INTERPRETATION */}

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<Brain />}
              title="ORCA Alert Interpretation"
            />

            <div className="mt-5 space-y-3">

              <Interpretation
                title="Wind"
                value={windSpeed}
                text={
                  windSpeed !== null
                    ? windSpeed > 30
                      ? "Strong winds may create difficult marine conditions and increase operational risk."
                      : windSpeed > 15
                      ? "Moderate winds are present and should be monitored during marine operations."
                      : "Wind conditions appear relatively calm based on the available data."
                    : "Wind information is unavailable."
                }
              />

              <Interpretation
                title="Wave Height"
                value={waveHeight}
                text={
                  waveHeight !== null
                    ? waveHeight > 2.5
                      ? "Higher waves may increase navigation difficulty and vessel safety risk."
                      : waveHeight > 1.5
                      ? "Moderate wave conditions are present."
                      : "Wave conditions appear relatively calm."
                    : "Wave information is unavailable."
                }
              />

              <Interpretation
                title="Rainfall"
                value={rainfall}
                text={
                  rainfall !== null
                    ? rainfall > 10
                      ? "Significant rainfall may reduce visibility and create difficult operating conditions."
                      : rainfall > 0
                      ? "Rainfall is present and should be monitored."
                      : "No significant rainfall is detected."
                    : "Rainfall information is unavailable."
                }
              />

            </div>

          </section>

          {/* SCIENTIFIC NOTE */}

          <section className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6">

            <div className="flex gap-4">

              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10">

                <Brain className="h-6 w-6 text-cyan-400" />

              </div>

              <div>

                <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                  Evidence-Aware Safety Support
                </p>

                <h2 className="mt-2 text-xl font-semibold">
                  ORCA combines available indicators before producing an alert assessment.
                </h2>

                <p className="mt-3 text-sm leading-6 text-slate-400">
                  {String(scientificNote)}
                </p>

                <p className="mt-3 text-xs leading-5 text-slate-600">
                  This system is decision support only and does
                  not replace official marine weather warnings,
                  navigation guidance or emergency services.
                </p>

              </div>

            </div>

          </section>

        </div>

      )}

    </div>
  );
}

/* =========================================================
   RESEARCH EVIDENCE
========================================================= */

function EvidencePage() {

  const [query, setQuery] = useState(
    "Why has Indian Oil Sardine productivity declined near Kerala?"
  );

  const [selectedDate, setSelectedDate] = useState(
    HISTORICAL_DATE
  );

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const analyzeEvidence = async () => {

    const cleanQuery = query.trim();

    if (!cleanQuery) {
      setError("Please enter a research question.");
      return;
    }

    if (!selectedDate) {
      setError("Please select an observation date.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const params = new URLSearchParams({
        query: cleanQuery,
        species: "Indian Oil Sardine",
        lat: String(DEFAULT_LAT),
        lon: String(DEFAULT_LON),
        date: selectedDate,
        salinity: "34",
      });

      const response = await fetch(
        `${API}/agentic-orca?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();

      setResult(data);

    } catch (err) {

      console.error("Evidence error:", err);

      setError(
        "Research evidence could not be loaded. Check that the FastAPI backend is running and that the requested date has available data."
      );

    } finally {

      setLoading(false);

    }

  };

  const evidence =
    Array.isArray(result?.evidence?.evidence)
      ? result.evidence.evidence
      : Array.isArray(result?.evidence)
        ? result.evidence
        : [];

  const reasoning =
    result?.reasoning ||
    {};

  const causal =
    result?.causal_reasoning ||
    {};

  const uncertainty =
    result?.uncertainty_analysis ||
    result?.uncertainty ||
    {};

  const llm =
    result?.llm ||
    {};

  const keyFindings =
    Array.isArray(llm.key_findings)
      ? llm.key_findings
      : [];

  const causalItems =
    Array.isArray(causal.causal_chain)
      ? causal.causal_chain
      : [];

  return (
    <div className="mx-auto max-w-7xl space-y-6">

      <PageHero
        icon={<Microscope />}
        title={
          <>
            Research <span className="text-cyan-400">Evidence</span>
          </>
        }
        description="Explore scientific evidence returned by the ORCA Evidence Agent and interpret it together with the selected observation date."
      />

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10">

            <Search className="h-5 w-5 text-cyan-400" />

          </div>

          <div>

            <h2 className="font-semibold">
              Research Evidence Query
            </h2>

            <p className="text-xs text-slate-500">
              Ask ORCA to retrieve and reason over marine evidence.
            </p>

          </div>

        </div>

        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={3}
          className="mt-5 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-sm text-white outline-none focus:border-cyan-500"
          placeholder="Ask about marine research evidence..."
        />

        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">

          <div>

            <label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-500">
              Observation Date
            </label>

            <input
              type="date"
              value={selectedDate}
              max={new Date().toISOString().split("T")[0]}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500"
            />

          </div>

          <div className="flex items-end">

            <div className="rounded-xl border border-slate-800 bg-slate-950 px-4 py-3">

              <p className="text-[11px] uppercase tracking-wider text-slate-500">
                Evidence mode
              </p>

              <p className="mt-1 text-sm font-semibold text-slate-300">
                Research + observation context
              </p>

            </div>

          </div>

        </div>

        <div className="mt-4 flex flex-wrap gap-2">

          <QuickQuestion
            text="Oil Sardine"
            onClick={() =>
              setQuery(
                "What research explains changes in Indian Oil Sardine productivity?"
              )
            }
          />

          <QuickQuestion
            text="Chlorophyll"
            onClick={() =>
              setQuery(
                "What does research say about chlorophyll and Indian Oil Sardine?"
              )
            }
          />

          <QuickQuestion
            text="Climate impact"
            onClick={() =>
              setQuery(
                "What environmental factors may affect Indian Oil Sardine?"
              )
            }
          />

        </div>

        <button
          onClick={analyzeEvidence}
          disabled={loading}
          className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
        >

          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              ORCA is retrieving evidence...
            </>
          ) : (
            <>
              <Microscope className="h-5 w-5" />
              Analyze Research Evidence
            </>
          )}

        </button>

      </section>

      {error && (
        <section className="rounded-xl border border-red-500/20 bg-red-500/5 p-5">

          <div className="flex items-start gap-3">

            <AlertTriangle className="h-5 w-5 text-red-400" />

            <div>

              <h3 className="font-semibold text-red-400">
                Evidence Analysis Failed
              </h3>

              <p className="mt-1 text-sm text-red-300/80">
                {error}
              </p>

            </div>

          </div>

        </section>
      )}

      {loading && (
        <LoadingBox
          title="ORCA is researching marine evidence"
          description="Query → Data → Evidence Agent → Causal analysis → Uncertainty"
        />
      )}

      {result && !loading && (

        <div className="space-y-6">

          <section className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6">

            <div className="flex flex-wrap items-start justify-between gap-5">

              <div>

                <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                  Research Assessment
                </p>

                <h2 className="mt-2 text-xl font-semibold text-slate-200">
                  {cleanMarkdown(
                    llm.answer ||
                    "ORCA completed the evidence assessment."
                  )}
                </h2>

              </div>

              <div className="rounded-xl border border-cyan-500/20 bg-slate-950 px-4 py-3">

                <p className="text-[11px] uppercase tracking-wider text-slate-500">
                  Observation date
                </p>

                <p className="mt-1 font-semibold text-cyan-400">
                  {result.date || selectedDate}
                </p>

              </div>

            </div>

          </section>

          <section className="grid gap-4 md:grid-cols-4">

            <MetricCard
              icon={<Microscope />}
              title="Evidence Items"
              value={String(evidence.length)}
              unit="items"
            />

            <MetricCard
              icon={<Fish />}
              title="Species"
              value={result.species || "Indian Oil Sardine"}
              unit=""
            />

            <MetricCard
              icon={<Brain />}
              title="Confidence"
              value={formatValue(
                uncertainty.confidence ??
                result.risk_analysis?.confidence ??
                null
              )}
              unit={
                (
                  uncertainty.confidence ??
                  result.risk_analysis?.confidence ??
                  null
                ) != null
                  ? "%"
                  : ""
              }
            />

            <MetricCard
              icon={<Shield />}
              title="Uncertainty"
              value={
                uncertainty.uncertainty_level ||
                "Unknown"
              }
              unit=""
              risk
            />

          </section>

          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <SectionTitle
              icon={<Microscope />}
              title="Scientific Evidence"
            />

            {evidence.length > 0 ? (

              <div className="mt-5 space-y-4">

                {evidence.map((item, index) => {

                  const title =
                    item?.topic ||
                    item?.title ||
                    item?.paper_title ||
                    item?.name ||
                    `Evidence ${index + 1}`;

                  const summary =
                    item?.finding ||
                    item?.summary ||
                    item?.description ||
                    item?.text ||
                    "Research evidence returned by the ORCA Evidence Agent.";

                  const source =
                    item?.source ||
                    item?.journal ||
                    item?.authors ||
                    "Marine research";

                  const evidenceType =
                    item?.evidence_type ||
                    "Research evidence";

                  const relevance =
                    item?.relevance ||
                    item?.relevance_score ||
                    null;

                  return (

                    <article
                      key={index}
                      className="rounded-2xl border border-slate-800 bg-slate-950 p-5"
                    >

                      <div className="flex items-start gap-4">

                        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10">

                          <Microscope className="h-5 w-5 text-cyan-400" />

                        </div>

                        <div className="min-w-0 flex-1">

                          <div className="flex flex-wrap items-center gap-2">

                            <span className="rounded-full border border-cyan-500/20 bg-cyan-500/5 px-2.5 py-1 text-[11px] text-cyan-400">
                              {evidenceType}
                            </span>

                            {relevance && (
                              <span className="rounded-full border border-emerald-500/20 bg-emerald-500/5 px-2.5 py-1 text-[11px] text-emerald-400">
                                Relevance: {String(relevance)}
                              </span>
                            )}

                          </div>

                          <h3 className="mt-3 text-base font-semibold leading-6 text-slate-200">
                            {String(title)}
                          </h3>

                          <p className="mt-2 text-xs leading-5 text-slate-500">
                            Source: {String(source)}
                          </p>

                          <div className="mt-4 rounded-xl bg-slate-900 p-4">

                            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                              Finding
                            </p>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                              {String(summary)}
                            </p>

                          </div>

                        </div>

                      </div>

                    </article>
                  );

                })}

              </div>

            ) : (

              <div className="mt-5 rounded-xl border border-amber-500/20 bg-amber-500/5 p-5">

                <div className="flex items-start gap-3">

                  <AlertTriangle className="h-5 w-5 text-amber-400" />

                  <div>

                    <h3 className="font-semibold text-amber-400">
                      No evidence items returned
                    </h3>

                    <p className="mt-1 text-sm leading-6 text-slate-400">
                      ORCA completed the request, but the current Evidence Agent did not return matching research items for this request.
                    </p>

                  </div>

                </div>

              </div>

            )}

          </section>

          {keyFindings.length > 0 && (

            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

              <SectionTitle
                icon={<Brain />}
                title="LLM Research Synthesis"
              />

              <div className="mt-5 space-y-3">

                {keyFindings.map(
                  (item, index) => (

                    <div
                      key={index}
                      className="flex gap-3 rounded-xl bg-slate-950 p-4"
                    >

                      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs font-bold text-cyan-400">
                        {index + 1}
                      </div>

                      <p className="text-sm leading-6 text-slate-300">
                        {String(item)}
                      </p>

                    </div>

                  )
                )}

              </div>

              {llm.recommendation && (

                <div className="mt-5 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4">

                  <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                    Recommendation
                  </p>

                  <p className="mt-2 text-sm leading-6 text-slate-300">
                    {String(llm.recommendation)}
                  </p>

                </div>

              )}

            </section>

          )}

          {Array.isArray(causalItems) &&
            causalItems.length > 0 && (

              <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <SectionTitle
                  icon={<Activity />}
                  title="Research Reasoning Chain"
                />

                <div className="mt-5 space-y-3">

                  {causalItems.map(
                    (item, index) => {

                      if (
                        item &&
                        typeof item === "object"
                      ) {

                        return (

                          <div
                            key={index}
                            className="rounded-xl bg-slate-950 p-4"
                          >

                            <div className="flex flex-wrap items-center gap-2">

                              <span className="rounded-lg border border-cyan-500/20 bg-cyan-500/5 px-3 py-2 text-sm text-cyan-300">
                                {item.factor || "Environmental factor"}
                              </span>

                              <span className="text-slate-600">
                                →
                              </span>

                              <span className="rounded-lg border border-cyan-500/20 bg-cyan-500/5 px-3 py-2 text-sm text-cyan-300">
                                {item.effect || "Potential ecological effect"}
                              </span>

                              {item.confidence && (
                                <span className="rounded-full border border-slate-700 px-2.5 py-1 text-[11px] text-slate-500">
                                  Confidence: {String(item.confidence)}
                                </span>
                              )}

                            </div>

                          </div>
                        );

                      }

                      return (

                        <div
                          key={index}
                          className="rounded-xl bg-slate-950 p-4 text-sm text-slate-300"
                        >
                          {String(item)}
                        </div>
                      );

                    }
                  )}

                </div>

                {causal.causal_inference_warning && (

                  <p className="mt-5 text-xs leading-5 text-amber-400/80">
                    {String(
                      causal.causal_inference_warning
                    )}
                  </p>

                )}

              </section>
            )}

          {Array.isArray(reasoning.reasoning) &&
            reasoning.reasoning.length > 0 && (

              <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <SectionTitle
                  icon={<Brain />}
                  title="Evidence-Based Reasoning"
                />

                <div className="mt-5 space-y-3">

                  {reasoning.reasoning.map(
                    (item, index) => (

                      <div
                        key={index}
                        className="flex gap-3 rounded-xl bg-slate-950 p-4"
                      >

                        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs font-bold text-cyan-400">
                          {index + 1}
                        </div>

                        <p className="text-sm leading-6 text-slate-300">
                          {String(item)}
                        </p>

                      </div>

                    )
                  )}

                </div>

              </section>
            )}

          <section className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-6">

            <div className="flex gap-4">

              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-amber-500/10">

                <AlertTriangle className="h-5 w-5 text-amber-400" />

              </div>

              <div>

                <p className="text-xs font-semibold uppercase tracking-wider text-amber-400">
                  Scientific Caution
                </p>

                <h2 className="mt-2 text-lg font-semibold text-slate-200">
                  Research evidence supports interpretation, not automatic causation.
                </h2>

                <p className="mt-3 text-sm leading-6 text-slate-400">
                  ORCA uses research findings together with available observations. A published relationship should be treated as evidence-informed context rather than proof that one environmental factor directly caused a particular fishery outcome.
                </p>

              </div>

            </div>

          </section>

        </div>
      )}

    </div>
  );
}

function ORCAResult({ data }) {

  const risk =
    data.risk_analysis ||
    data.risk ||
    {};

  const uncertainty =
    data.uncertainty_analysis ||
    data.uncertainty ||
    {};

  const evidence =
    Array.isArray(data.evidence?.evidence)
      ? data.evidence.evidence
      : Array.isArray(data.evidence)
        ? data.evidence
        : [];

  const planning =
    data.llm_plan ||
    data.planner ||
    data.execution_plan ||
    data.planning ||
    {};

  const debate =
    data.agent_debate ||
    data.debate ||
    {};

  const reasoning =
    data.reasoning ||
    {};

  const causal =
    data.causal_reasoning ||
    {};

  const causalChain =
    Array.isArray(causal.causal_chain)
      ? causal.causal_chain
      : Array.isArray(reasoning.causal_chain)
        ? reasoning.causal_chain
        : [];

  const reasoningPoints =
    Array.isArray(reasoning.reasoning)
      ? reasoning.reasoning
      : [];

  const llm =
    data.llm ||
    {};

  const overallRisk =
    risk.overall_risk ||
    reasoning.overall_risk ||
    data.fish_analysis?.risk ||
    "Unknown";

  const confidence =
    uncertainty.confidence ??
    reasoning.confidence ??
    risk.confidence ??
    null;

  const temperature =
    data.observations?.sea_surface_temperature ??
    data.ocean_analysis?.temperature ??
    data.fish_analysis?.temperature ??
    null;

  const chlorophyll =
    data.observations?.chlorophyll ??
    data.ocean_analysis?.chlorophyll ??
    data.fish_analysis?.chlorophyll ??
    null;

  const species =
    data.species ||
    data.fish_analysis?.species ||
    "Indian Oil Sardine";

  const requestedDate =
    data.date ||
    data.llm_orchestration?.trusted_context?.observation_date ||
    "Unknown";

  const fallbackActive =
    Boolean(
      data?.fallback ||
      data?.llm_orchestration?.llm_planning_failed ||
      data?.llm?.fallback ||
      data?.llm?.llm_used === false
    );

  return (
    <div className="space-y-6">

      {fallbackActive && (
        <div className="flex items-center justify-between gap-4 rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-amber-300">
          <div className="flex items-center gap-3">
            <span className="relative flex h-3 w-3 shrink-0">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber-400 opacity-75" />
              <span className="relative inline-flex h-3 w-3 rounded-full bg-amber-500" />
            </span>
            <div>
              <p className="text-sm font-semibold">
                ⚡ Deterministic Expert Mode Active
              </p>
              <p className="text-xs leading-5 text-amber-400/80">
                LLM orchestration is unavailable or rate-limited. ORCA is executing its deterministic analysis pipeline using available environmental observations and rule-based specialist agents.
              </p>
            </div>
          </div>
          <span className="shrink-0 rounded-md bg-amber-500/20 px-2.5 py-1 font-mono text-xs font-bold">
            DATA-GROUNDED MODE
          </span>
        </div>
      )}

      <section className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6">

        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">

          <div className="flex gap-4">

            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10">

              <Brain className="h-6 w-6 text-cyan-400" />

            </div>

            <div>

              <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                ORCA Final Assessment
              </p>

              <h2 className="mt-2 text-xl font-semibold leading-8 text-slate-200">
                {cleanMarkdown(
                  llm.answer ||
                  getSummary(data)
                )}
              </h2>

            </div>

          </div>

          <div className="shrink-0 rounded-xl border border-slate-800 bg-slate-950 px-4 py-3">

            <p className="text-[11px] uppercase tracking-wider text-slate-500">
              Observation date
            </p>

            <p className="mt-1 font-semibold text-cyan-400">
              {requestedDate}
            </p>

          </div>

        </div>

        {llm.model && (

          <div className="mt-5 flex flex-wrap items-center gap-2 text-xs text-slate-500">

            <span>
              LLM:
            </span>

            <span className="rounded-full border border-cyan-500/20 bg-cyan-500/5 px-3 py-1 text-cyan-400">
              {String(llm.model)}
            </span>

            {llm.rounds !== undefined && (
              <span className="rounded-full border border-slate-800 bg-slate-950 px-3 py-1">
                Tool rounds: {String(llm.rounds)}
              </span>
            )}

          </div>
        )}

      </section>

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <SectionTitle
          icon={<Brain />}
          title="Agentic Planning"
        />

        <div className="mt-5 flex flex-wrap gap-2">

          {(planning.selected_agents || []).map(
            (agent) => (

              <span
                key={agent}
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-slate-300"
              >
                {agent}
              </span>

            )
          )}

        </div>

      </section>

      <section className="grid gap-4 md:grid-cols-4">

        <MetricCard
          icon={<Waves />}
          title="Sea Surface Temperature"
          value={formatValue(temperature)}
          unit="°C"
        />

        <MetricCard
          icon={<Activity />}
          title="Chlorophyll"
          value={formatValue(chlorophyll)}
          unit="mg/m³"
        />

        <MetricCard
          icon={<Fish />}
          title="Species"
          value={species}
          unit=""
        />

        <MetricCard
          icon={<Shield />}
          title="Overall Risk"
          value={overallRisk}
          unit=""
          risk
        />

      </section>

      <section className="grid gap-6 md:grid-cols-2">

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Brain />}
            title="Key Findings"
          />

          <div className="mt-5 space-y-3">

            {Array.isArray(llm.key_findings) &&
            llm.key_findings.length > 0 ? (

              llm.key_findings.map(
                (item, index) => (

                  <div
                    key={index}
                    className="flex gap-3 rounded-xl bg-slate-950 p-4"
                  >

                    <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs font-bold text-cyan-400">
                      {index + 1}
                    </div>

                    <p className="text-sm leading-6 text-slate-300">
                      {String(item)}
                    </p>

                  </div>

                )
              )

            ) : reasoningPoints.length > 0 ? (

              reasoningPoints.map(
                (item, index) => (

                  <div
                    key={index}
                    className="flex gap-3 rounded-xl bg-slate-950 p-4"
                  >

                    <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs font-bold text-cyan-400">
                      {index + 1}
                    </div>

                    <p className="text-sm leading-6 text-slate-300">
                      {String(item)}
                    </p>

                  </div>

                )
              )

            ) : (

              <p className="rounded-xl bg-slate-950 p-4 text-sm text-slate-500">
                No additional reasoning points were returned.
              </p>

            )}

          </div>

        </section>

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Activity />}
            title="Confidence & Uncertainty"
          />

          <div className="mt-5 rounded-xl bg-slate-950 p-5">

            <p className="text-xs uppercase text-slate-500">
              Confidence
            </p>

            <p className="mt-2 text-3xl font-bold text-cyan-400">

              {confidence !== null
                ? `${confidence}%`
                : "N/A"}

            </p>

            {confidence !== null && (

              <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-800">

                <div
                  className="h-full rounded-full bg-cyan-400"
                  style={{
                    width: `${Math.min(
                      Math.max(Number(confidence), 0),
                      100
                    )}%`,
                  }}
                />

              </div>

            )}

            {uncertainty.uncertainty_level && (

              <p className="mt-4 text-sm text-slate-400">
                {String(
                  uncertainty.uncertainty_level
                )}
              </p>

            )}

            {Array.isArray(
              uncertainty.uncertainty_reasons
            ) &&
            uncertainty.uncertainty_reasons.length > 0 && (

              <div className="mt-4 space-y-2">

                {uncertainty.uncertainty_reasons.map(
                  (item, index) => (

                    <p
                      key={index}
                      className="text-xs leading-5 text-slate-500"
                    >
                      • {String(item)}
                    </p>

                  )
                )}

              </div>

            )}

          </div>

        </section>

      </section>

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <SectionTitle
          icon={<Fish />}
          title="Fish Analysis"
        />

        <div className="mt-5 grid gap-4 md:grid-cols-2">

          <InfoBox
            title="Species"
            value={species}
          />

          <InfoBox
            title="Environmental Risk"
            value={
              data.fish_analysis?.risk ||
              "Unknown"
            }
          />

          <InfoBox
            title="Observation Date"
            value={requestedDate}
          />

          <InfoBox
            title="Location"
            value={
              data.location
                ? `${data.location.latitude}, ${data.location.longitude}`
                : "Kerala / Arabian Sea"
            }
          />

        </div>

      </section>

      {data.ocean_analysis && (

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Waves />}
            title="Ocean Assessment"
          />

          <div className="mt-5 grid gap-4 md:grid-cols-3">

            <InfoBox
              title="Ocean Condition"
              value={
                data.ocean_analysis.ocean_condition ||
                "Unknown"
              }
            />

            <InfoBox
              title="Stress Score"
              value={formatValue(
                data.ocean_analysis.stress_score
              )}
            />

            <InfoBox
              title="Salinity"
              value={`${formatValue(
                data.ocean_analysis.salinity ??
                data.observations?.salinity ??
                null
              )} PSU`}
            />

          </div>

        </section>

      )}

      {data.ecosystem_analysis && (

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Globe2 />}
            title="Ecosystem Assessment"
          />

          <div className="mt-5 rounded-xl bg-slate-950 p-5">

            <p className="text-xs uppercase tracking-wider text-slate-500">
              Ecosystem Status
            </p>

            <p className="mt-2 text-2xl font-bold text-cyan-400">
              {data.ecosystem_analysis.ecosystem_status ||
                "Unknown"}
            </p>

            {Array.isArray(
              data.ecosystem_analysis.factors
            ) && (

              <div className="mt-4 space-y-2">

                {data.ecosystem_analysis.factors.map(
                  (item, index) => (

                    <p
                      key={index}
                      className="text-sm text-slate-400"
                    >
                      • {String(item)}
                    </p>

                  )
                )}

              </div>

            )}

          </div>

        </section>

      )}

      <section className="grid gap-6 md:grid-cols-2">

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Shield />}
            title="Risk Assessment"
          />

          <div className="mt-5 flex items-center justify-between rounded-xl bg-slate-950 p-5">

            <div>

              <p className="text-xs uppercase text-slate-500">
                Overall Risk
              </p>

              <p className="mt-2 text-2xl font-bold">
                {overallRisk}
              </p>

              {risk.confidence !== undefined && (

                <p className="mt-2 text-xs text-slate-500">
                  Agent confidence: {String(
                    risk.confidence
                  )}%
                </p>

              )}

            </div>

            <RiskBadge risk={overallRisk} />

          </div>

        </section>

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Microscope />}
            title="Research Evidence"
          />

          <div className="mt-5 rounded-xl bg-slate-950 p-5">

            <p className="text-3xl font-bold text-cyan-400">
              {evidence.length}
            </p>

            <p className="mt-1 text-sm text-slate-500">
              evidence items returned by the ORCA Evidence Agent
            </p>

          </div>

        </section>

      </section>

      {evidence.length > 0 && (

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Microscope />}
            title="Scientific Evidence"
          />

          <div className="mt-5 space-y-4">

            {evidence.map(
              (item, index) => (

                <article
                  key={index}
                  className="rounded-2xl border border-slate-800 bg-slate-950 p-5"
                >

                  <div className="flex items-start gap-4">

                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10">

                      <CheckCircle className="h-5 w-5 text-emerald-400" />

                    </div>

                    <div className="min-w-0 flex-1">

                      <div className="flex flex-wrap items-center gap-2">

                        <span className="rounded-full border border-cyan-500/20 bg-cyan-500/5 px-2.5 py-1 text-[11px] text-cyan-400">
                          {item?.evidence_type ||
                            "Research evidence"}
                        </span>

                        {item?.relevance && (
                          <span className="rounded-full border border-emerald-500/20 bg-emerald-500/5 px-2.5 py-1 text-[11px] text-emerald-400">
                            {String(item.relevance)}
                          </span>
                        )}

                      </div>

                      <h3 className="mt-3 text-base font-semibold leading-6 text-slate-200">
                        {String(
                          item?.topic ||
                          item?.title ||
                          item?.paper_title ||
                          "Research evidence"
                        )}
                      </h3>

                      <p className="mt-2 text-xs leading-5 text-slate-500">
                        Source: {String(
                          item?.source ||
                          "Marine research"
                        )}
                      </p>

                      <div className="mt-4 rounded-xl bg-slate-900 p-4">

                        <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                          Finding
                        </p>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                          {String(
                            item?.finding ||
                            item?.summary ||
                            item?.description ||
                            "No finding text was returned."
                          )}
                        </p>

                      </div>

                    </div>

                  </div>

                </article>

              )
            )}

          </div>

        </section>

      )}

      {causalChain.length > 0 && (

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <SectionTitle
            icon={<Activity />}
            title="Causal Reasoning"
          />

          <div className="mt-5 space-y-3">

            {causalChain.map(
              (item, index) => {

                if (
                  item &&
                  typeof item === "object"
                ) {

                  return (

                    <div
                      key={index}
                      className="rounded-xl bg-slate-950 p-4"
                    >

                      <div className="flex flex-wrap items-center gap-3">

                        <span className="rounded-lg border border-cyan-500/20 bg-cyan-500/5 px-3 py-2 text-sm text-cyan-300">
                          {item.factor ||
                            "Environmental factor"}
                        </span>

                        <span className="text-slate-600">
                          →
                        </span>

                        <span className="rounded-lg border border-cyan-500/20 bg-cyan-500/5 px-3 py-2 text-sm text-cyan-300">
                          {item.effect ||
                            "Potential ecological effect"}
                        </span>

                        {item.confidence && (

                          <span className="rounded-full border border-slate-700 px-2.5 py-1 text-[11px] text-slate-500">
                            {String(
                              item.confidence
                            )}
                          </span>

                        )}

                      </div>

                    </div>
                  );

                }

                return (

                  <div
                    key={index}
                    className="rounded-xl bg-slate-950 p-4 text-sm text-slate-300"
                  >
                    {String(item)}
                  </div>
                );

              }
            )}

          </div>

          {causal.causal_inference_warning && (

            <div className="mt-5 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4">

              <p className="text-xs leading-5 text-amber-400">
                {String(
                  causal.causal_inference_warning
                )}
              </p>

            </div>

          )}

        </section>

      )}

      {llm.recommendation && (

        <section className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6">

          <SectionTitle
            icon={<Brain />}
            title="ORCA Recommendation"
          />

          <p className="mt-4 text-sm leading-7 text-slate-300">
            {String(llm.recommendation)}
          </p>

        </section>

      )}

      <section className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-6">

        <div className="flex gap-4">

          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-amber-500/10">

            <AlertTriangle className="h-5 w-5 text-amber-400" />

          </div>

          <div>

            <p className="text-xs font-semibold uppercase tracking-wider text-amber-400">
              Scientific Caution
            </p>

            <h2 className="mt-2 text-lg font-semibold text-slate-200">
              Research evidence supports interpretation, not automatic causation.
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-400">
              ORCA uses research findings together with available observations. Published relationships are treated as evidence-informed context rather than proof that one environmental factor directly caused a particular fishery outcome.
            </p>

          </div>

        </div>

      </section>

    </div>
  );
}

/* =========================================================
   LOADING
========================================================= */

function LoadingORCA() {

  return (
    <LoadingBox
      title="ORCA is coordinating its agents"
      description="Planning → Data retrieval → Analysis → Reasoning"
    />
  );

}

function LoadingBox({
  title,
  description,
}) {

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-8">

      <div className="flex items-center gap-4">

        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500/10">

          <Brain className="h-6 w-6 animate-pulse text-cyan-400" />

        </div>

        <div>

          <h3 className="font-semibold">
            {title}
          </h3>

          <p className="mt-1 text-sm text-slate-500">
            {description}
          </p>

        </div>

      </div>

      <div className="mt-6 grid gap-3 md:grid-cols-4">

        {[
          "Planner",
          "Marine Data",
          "Specialist Agents",
          "Reasoning",
        ].map((agent) => (

          <div
            key={agent}
            className="animate-pulse rounded-xl border border-slate-800 bg-slate-950 p-4"
          >

            <div className="h-3 w-20 rounded bg-slate-800" />

            <div className="mt-3 h-2 w-full rounded bg-slate-800" />

          </div>

        ))}

      </div>

    </section>
  );
}

/* =========================================================
   PAGE HERO
========================================================= */

function PageHero({
  icon,
  title,
  description,
}) {

  return (
    <section className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-8">

      <div className="max-w-3xl">

        <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
          {icon}
        </div>

        <h1 className="text-4xl font-bold tracking-tight">
          {title}
        </h1>

        <p className="mt-4 leading-7 text-slate-400">
          {description}
        </p>

      </div>

    </section>
  );
}

/* =========================================================
   COMPONENTS
========================================================= */

function SectionTitle({
  icon,
  title,
}) {

  return (
    <div className="flex items-center gap-3">

      <div className="text-cyan-400">
        {icon}
      </div>

      <h2 className="text-lg font-semibold">
        {title}
      </h2>

    </div>
  );
}

function MetricCard({
  icon,
  title,
  value,
  unit,
  risk = false,
}) {

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

      <div className="flex items-center justify-between">

        <div className="text-cyan-400">
          {icon}
        </div>

        {risk && (
          <RiskBadge risk={value} />
        )}

      </div>

      <p className="mt-4 text-xs uppercase tracking-wider text-slate-500">
        {title}
      </p>

      <div className="mt-2 flex items-baseline gap-2">

        <p className="text-2xl font-bold">
          {value}
        </p>

        {unit && (
          <span className="text-xs text-slate-500">
            {unit}
          </span>
        )}

      </div>

    </div>
  );
}

function InfoBox({
  title,
  value,
}) {

  return (
    <div className="rounded-xl bg-slate-950 p-4">

      <p className="text-xs uppercase tracking-wider text-slate-500">
        {title}
      </p>

      <p className="mt-2 font-semibold text-slate-200">
        {value}
      </p>

    </div>
  );
}

function ModuleCard({
  icon,
  title,
  description,
  onClick,
}) {

  return (
    <button
      onClick={onClick}
      className="group rounded-2xl border border-slate-800 bg-slate-950 p-5 text-left transition hover:-translate-y-1 hover:border-cyan-500/40"
    >

      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400 transition group-hover:bg-cyan-500/20">
        {icon}
      </div>

      <h3 className="mt-4 font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-500">
        {description}
      </p>

    </button>
  );
}

function AgentCard({
  icon,
  name,
  description,
}) {

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950 p-5">

      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
        {icon}
      </div>

      <h3 className="mt-4 font-semibold">
        {name}
      </h3>

      <p className="mt-2 text-xs leading-5 text-slate-500">
        {description}
      </p>

      <div className="mt-4 flex items-center gap-2">

        <div className="h-2 w-2 rounded-full bg-emerald-400" />

        <span className="text-xs text-emerald-400">
          Active
        </span>

      </div>

    </div>
  );
}

function QuickQuestion({
  text,
  onClick,
}) {

  return (
    <button
      onClick={onClick}
      className="rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-400 hover:border-cyan-500 hover:text-cyan-400"
    >
      {text}
    </button>
  );
}

function Interpretation({
  title,
  value,
  text,
}) {

  return (
    <div className="rounded-xl bg-slate-950 p-4">

      <div className="flex items-center justify-between gap-4">

        <div>

          <p className="font-semibold text-slate-200">
            {title}
          </p>

          <p className="mt-1 text-sm leading-6 text-slate-500">
            {text}
          </p>

        </div>

        <p className="shrink-0 text-lg font-bold text-cyan-400">
          {formatValue(value)}
        </p>

      </div>

    </div>
  );
}

function RiskBadge({
  risk,
}) {

  const normalized =
    String(risk).toLowerCase();

  let classes =
    "border-slate-700 bg-slate-900 text-slate-400";

  if (
    normalized.includes("high") ||
    normalized.includes("risk")
  ) {

    classes =
      "border-red-500/20 bg-red-500/10 text-red-400";

  } else if (
    normalized.includes("moderate") ||
    normalized.includes("caution")
  ) {

    classes =
      "border-amber-500/20 bg-amber-500/10 text-amber-400";

  } else if (
    normalized.includes("low") ||
    normalized.includes("safe") ||
    normalized.includes("stable") ||
    normalized.includes("normal") ||
    normalized.includes("clear")
  ) {

    classes =
      "border-emerald-500/20 bg-emerald-500/10 text-emerald-400";

  }

  return (
    <span
      className={`rounded-full border px-3 py-1 text-xs font-semibold ${classes}`}
    >
      {risk}
    </span>
  );
}

/* =========================================================
   PLACEHOLDER
========================================================= */

function PlaceholderPage({
  icon,
  title,
  description,
}) {

  return (
    <div className="mx-auto max-w-6xl">

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-10">

        <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
          {icon}
        </div>

        <h1 className="mt-6 text-3xl font-bold">
          {title}
        </h1>

        <p className="mt-3 max-w-2xl text-slate-400">
          {description}
        </p>

        <div className="mt-8 rounded-xl border border-dashed border-slate-700 bg-slate-950 p-8 text-center">

          <p className="text-sm text-slate-500">
            ORCA module ready for backend integration.
          </p>

          <p className="mt-2 text-xs text-slate-700">
            This module will be connected next.
          </p>

        </div>

      </section>

    </div>
  );
}

/* =========================================================
   HELPERS
========================================================= */

function formatValue(value) {

  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return "N/A";
  }

  if (typeof value === "number") {

    return Number.isInteger(value)
      ? value
      : value.toFixed(2);

  }

  return value;
}

function getSummary(data) {

  if (
    data?.llm?.answer
  ) {

    return cleanMarkdown(
      data.llm.answer
    );

  }

  const reasoning =
    data.reasoning || {};

  if (
    Array.isArray(reasoning.reasoning) &&
    reasoning.reasoning.length > 0
  ) {

    return String(
      reasoning.reasoning[0]
    );

  }

  if (data.final_answer) {

    return cleanMarkdown(
      data.final_answer
    );

  }

  if (
    data.fish_analysis?.scientific_note
  ) {

    return data.fish_analysis.scientific_note;

  }

  return "ORCA completed the marine ecosystem assessment.";
}

function cleanMarkdown(text) {

  if (!text) return "";

  return String(text)
    .replace(
      /```[\s\S]*?```/g,
      ""
    )
    .replace(
      /^#+\s*/gm,
      ""
    )
    .replace(
      /\*\*(.*?)\*\*/g,
      "$1"
    )
    .replace(
      /\*(.*?)\*/g,
      "$1"
    )
    .replace(
      /^\s*[-•]\s*/gm,
      ""
    )
    .replace(
      /svg/gi,
      ""
    )
    .replace(
      /\n{3,}/g,
      "\n\n"
    )
    .trim();
}

export default App;

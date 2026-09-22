# ORCA — Ocean Reasoning with Collaborative Agents
### *Deterministic Marine Decision Engine with a Constrained Multi-Agent Reasoning Layer*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%202.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![Leaflet](https://img.shields.io/badge/GIS-Leaflet-199900?style=flat-square&logo=leaflet)](https://leafletjs.com/)
[![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini%201.5-8E75B2?style=flat-square&logo=google)](https://ai.google.dev/)
[![Live Status](https://img.shields.io/badge/System-Healthy%20%26%20Operational-brightgreen?style=flat-square)](https://orca-marine-ecosystem-intelligence-1.onrender.com/health)
[![SIH 2026](https://img.shields.io/badge/SIH%202026-SIH26176-orange?style=flat-square)](https://sih.gov.in/)

> **Team:** HashBoom | **Theme:** Space Technology / Disaster Management | **Organization Fit:** ISRO & INCOIS

---

## 🌊 Executive Summary & Value Proposition

**ORCA** addresses the operational and safety gaps in modern marine advisory delivery across India’s **8,100 km coastline**. While **INCOIS (Indian National Centre for Ocean Information Services)** generates high-fidelity satellite Potential Fishing Zone (PFZ) advisories, traditional small-craft artisanal fishers face three critical hurdles:
1. **Lack of species-specific biological suitability** (a PFZ thermal front may exceed the thermal tolerance of local target species like Indian Oil Sardine).
2. **Absence of vessel-class wave/wind safety context** (high-catch zones are often inaccessible to small motorized craft under heavy swell).
3. **Black-box delivery without explainability** (static SMS/charts do not explain *why* an area is viable or *how confident* the data is when cloud cover blinds optical satellites).

**ORCA augments INCOIS advisories** by wrapping them in a **15-Agent Collaborative Intelligence Layer** backed by a **zero-LLM deterministic fallback engine**. It converts fragmented satellite feeds into a single evidence-grounded go/no-go answer in seconds.

---

## 🛰️ System Architecture & Dual-Path Redundancy

To ensure strict zero-hallucination compliance for mission-critical maritime safety, ORCA implements a **Dual-Path Architecture**:

```
                              ┌──────────────────────────────────────────────┐
                              │          Live Ingestion Pipeline             │
                              │  • NOAA CoastWatch MUR SST (~1km, 0.01°)     │
                              │  • INCOIS Oceansat-2 OCM Chlorophyll-a (360m)│
                              │  • Open-Meteo Marine (Hourly Swell/Wind)     │
                              └──────────────────────┬───────────────────────┘
                                                     │
                                                     ▼
                              ┌──────────────────────────────────────────────┐
                              │            Trusted Context Lock              │
                              │  (Locks lat, lon, date, species & raw data)  │
                              └──────────────────────┬───────────────────────┘
                                                     │
                        ┌────────────────────────────┴────────────────────────────┐
                        │                                                         │
                        ▼                                                         ▼
       ┌─────────────────────────────────┐                       ┌─────────────────────────────────┐
       │    Primary: Gemini 1.5 Pro      │                       │     Deterministic Fallback      │
       │    Agentic Tool-Calling Loop    │                       │     Zero-LLM Marine Rules Engine│
       │ (15 Specialized Marine Agents)  │                       │ (Direct SST/Chl/Safety Engine)  │
       └────────────────┬────────────────┘                       └────────────────┬────────────────┘
                        │                                                         │
                        │        (Auto-Fallback if LLM Timeout / Rate Limit)      │
                        └────────────────────────────► ◄──────────────────────────┘
                                                     │
                                                     ▼
                              ┌──────────────────────────────────────────────┐
                              │          Consolidated Advisory Output        │
                              │ • Biological Suitability Index (Species-fit) │
                              │ • Vessel-Class Safety Check (Aditya et al.)  │
                              │ • Epistemic Confidence Score & Evidence Chain│
                              │ • Interactive Leaflet GIS Map & Polyline Route│
                              └──────────────────────────────────────────────┘
```

### 🔒 Key Architectural Safeguards
* **Trusted Context Lock:** Coordinates, timestamps, and ocean observations are locked before calling the language model, eliminating coordinate hallucination.
* **Deterministic Dual Path:** If the LLM provider experiences network latency (>1.2s) or rate-limiting, the deterministic mathematical rules engine outputs the advisory with 100% operational uptime.

---

## 🤖 15 Specialized Marine Agents

ORCA coordinates 15 modular agent tools across data ingestion, environmental analysis, and safety decisioning:

| Category | Agent / Tool Identifier | Operational Scope & Capabilities |
| :--- | :--- | :--- |
| **Data Ingestion** | `get_marine_observations` | Live SST, Chlorophyll-a, and Salinity ingestion via ERDDAP endpoints |
| | `get_marine_weather` | Real-time swell height, wind speed, wave period, and precipitation |
| **Environmental** | `run_fish_agent` | Biological envelope comparison (e.g., Sardine thermal range 26–29°C) |
| | `run_ocean_agent` | Thermal gradient and oceanographic upwelling front detection |
| | `run_ecosystem_agent` | Multi-trophic ecosystem health and trophic stability evaluation |
| | `run_weather_agent` | Meteorological safety and sea-state analysis |
| | `run_risk_agent` | Integrated multi-hazard risk assessment |
| **Reasoning & QA** | `run_evidence_agent` | Grounds conclusions in peer-reviewed marine literature (*Kripa et al., Nayak et al.*) |
| | `run_uncertainty_agent` | Quantifies epistemic confidence under satellite cloud-cover data gaps |
| | `run_reasoning_agent` | Generates step-by-step causal explanation chains |
| | `run_causal_agent` | Isolates primary environmental drivers of observed anomalies |
| | `run_debate_agent` | Resolves conflicting signals (e.g., high food density vs. unsafe swell) |
| **Safety & Routing**| `run_alert_agent` | Generates location-specific maritime safety alerts |
| | `run_route_agent` | Dynamic wave/wind-minimized waypoint routing |
| | `run_geofence_agent` | Enforces maritime boundaries and Exclusive Economic Zone (EEZ) compliance |

---

## 🔌 API Endpoint Catalog (FastAPI 2.0)

ORCA provides **20 verified, production-ready REST API endpoints**:

```
├── System & Health
│   ├── GET /                                -> System identity & version info
│   ├── GET /health                          -> Active health check & 15-tool registry status
│   └── GET /llm-status                      -> Active LLM model & tool binding status
│
├── Multi-Agent Orchestration & Reasoning
│   ├── GET /agentic-orca                    -> Full 15-agent workflow execution
│   └── GET /chat                            -> Context-grounded oceanographic chat assistant
│
├── Oceanographic & Biological Analysis
│   ├── GET /orca-location-analysis          -> Comprehensive lat/lon/species/date analysis
│   ├── GET /fish-analysis                   -> Species suitability scoring
│   ├── GET /ocean-analysis                  -> Thermal and salinity condition analysis
│   ├── GET /ecosystem-analysis              -> Multi-species ecosystem stability
│   ├── GET /risk-analysis                   -> Multi-factor risk scoring
│   └── GET /ocean-location-analysis         -> Satellite parameter extraction
│
├── Spatial PFZ & Mapping
│   ├── GET /spatial-pfz                     -> Bounding-box spatial grid scoring
│   └── GET /pfz-map                         -> Leaflet-ready GeoJSON candidate PFZ zones
│
└── Maritime Safety & Navigation
    ├── GET /route-analysis                  -> Vessel-class-specific route analysis (OBM vs Trawler)
    ├── GET /safe-route                      -> Waypoint route calculation with wave penalty
    ├── GET /safety-decision                 -> Operational go/no-go safety advisories
    ├── GET /geofence                        -> National maritime EEZ boundary validation
    ├── GET /alerts                          -> Real-time coastal weather and hazard alerts
    └── GET /weather-location-analysis       -> Localized marine weather metrics
```

---

## 🔬 Scientific Validation & Baseline Comparison

ORCA explicitly augments official **INCOIS Potential Fishing Zone (PFZ)** baselines:

| Advisory Dimension | Official INCOIS PFZ Baseline | ORCA Augmented Decision Layer |
| :--- | :--- | :--- |
| **Core Location** | Identifies chlorophyll / SST thermal fronts | Ingests official INCOIS PFZ coordinates as baseline |
| **Species Context** | General pelagic fish aggregation | Species-specific thermal suitability (*Kripa et al., 2018*) |
| **Vessel Safety** | Broad coastal sea-state forecasts | Vessel-class-specific wave/wind limits (*Aditya et al., 2020 SVAS*) |
| **Uncertainty** | Binary / zone boundary maps | Explicit Epistemic Confidence scoring when data is cloud-obscured |
| **Explainability** | Static PDF maps / SMS notifications | Conversational causal reasoning (*Why*, *How Safe*, *How Confident*) |

---

## 🚀 Quickstart & Local Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/soorya011-sp/ORCA-Marine-Ecosystem-Intelligence.git
cd ORCA-Marine-Ecosystem-Intelligence
```

### 2. Run Backend (FastAPI)
```bash
cd backend
python -m venv venv
# Activate environment:
# Windows: venv\Scripts\activate | Linux/macOS: source venv/bin/activate
pip install -r requirements.txt

# Start backend server
uvicorn main:app --reload --port 8000
```
* Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`
* Health Check: `http://localhost:8000/health`

### 3. Run Frontend (React + Vite)
```bash
cd ../frontend
npm install
npm run dev
```
* Dashboard will be live at: `http://localhost:5173`

---

## 🌐 Live Platform & Demo Credentials

* **Live Frontend:** [https://orca-marine-ecosystem-intelligence-2.onrender.com/](https://orca-marine-ecosystem-intelligence-2.onrender.com/)
* **Live API Backend:** [https://orca-marine-ecosystem-intelligence-1.onrender.com/health](https://orca-marine-ecosystem-intelligence-1.onrender.com/health)
* **SIH Demo Credentials:**
  * **Email:** `admin@orca.ai`
  * **Password:** `orca123`

*(Note: Free cloud hosting may take ~20 seconds to spin up on initial cold start).*

---

## 👥 Team Information
* **Team:** HashBoom
* **Hackathon:** Smart India Hackathon (SIH) 2026
* **Problem Statement ID:** SIH26176
* **Category:** Software / Space Technology

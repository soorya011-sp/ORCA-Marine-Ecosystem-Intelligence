import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

# ============================================================
# DATA SOURCES
# ============================================================

NOAA_SST_URL = (
    "https://coastwatch.pfeg.noaa.gov/erddap/"
    "griddap/jplMURSST41.json"
)

INCOIS_CHL_URL = (
    "https://erddap.incois.gov.in/erddap/griddap/"
    "incois_oceansat2_datasets.json"
)

REQUEST_TIMEOUT = 30


# ============================================================
# HELPER
# ============================================================

def safe_float(value):
    """
    Convert a value to float safely.
    """
    try:
        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()

        if value in ["", "null", "None"]:
            return None

        return float(value)

    except (ValueError, TypeError):
        return None


# ============================================================
# SINGLE POINT - SST
# ============================================================

def get_sst(lat, lon, date):
    """
    Fetch SST for one geographic point.
    """
    query = (
        f"?analysed_sst"
        f"[({date}T00:00:00Z)]"
        f"[({lat})]"
        f"[({lon})]"
    )

    try:
        response = requests.get(
            NOAA_SST_URL + query,
            timeout=15
        )
        response.raise_for_status()

        data = response.json()

        return {
            "source": "NOAA CoastWatch",
            "variable": "sea_surface_temperature",
            "latitude": lat,
            "longitude": lon,
            "date": date,
            "data": data
        }

    except Exception as noaa_error:
        # Fallback to Open-Meteo Marine API if NOAA is unavailable or times out
        try:
            response = requests.get(
                "https://marine-api.open-meteo.com/v1/marine",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "sea_surface_temperature"
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            temperature = data.get("current", {}).get(
                "sea_surface_temperature"
            )

            return {
                "source": "Open-Meteo Marine",
                "variable": "sea_surface_temperature",
                "latitude": lat,
                "longitude": lon,
                "date": data.get("current", {}).get("time", date),
                "value": temperature,
                "data": data,
                "fallback": True
            }

        except Exception as fallback_error:
            return {
                "source": "NOAA CoastWatch",
                "variable": "sea_surface_temperature",
                "latitude": lat,
                "longitude": lon,
                "date": date,
                "error": f"NOAA: {noaa_error}; Fallback: {fallback_error}"
            }


# ============================================================
# SINGLE POINT - CHLOROPHYLL
# ============================================================

def get_chlorophyll(lat, lon, date):
    """
    Fetch chlorophyll for one geographic point.
    """
    query = (
        f"?CHL"
        f"[({date}T00:00:00Z)]"
        f"[({lat})]"
        f"[({lon})]"
    )

    try:
        response = requests.get(
            INCOIS_CHL_URL + query,
            timeout=15,
            verify=False
        )
        response.raise_for_status()

        data = response.json()

        return {
            "source": "INCOIS",
            "variable": "chlorophyll",
            "latitude": lat,
            "longitude": lon,
            "date": date,
            "data": data
        }

    except Exception as e:
        return {
            "source": "INCOIS",
            "variable": "chlorophyll",
            "latitude": lat,
            "longitude": lon,
            "date": date,
            "error": str(e)
        }


# ============================================================
# EXTRACTION HELPERS (WITH KELVIN -> CELSIUS CONVERSION)
# ============================================================

def extract_value(result):
    """
    Extract the first numeric value from an ERDDAP response.
    Converts Kelvin to Celsius for SST if value > 200.
    """
    try:
        val = None

        if isinstance(result, dict):
            if result.get("value") is not None:
                val = safe_float(result["value"])
            else:
                rows = result.get("data", {}).get("table", {}).get("rows", [])
                if rows:
                    val = safe_float(rows[0][-1])

        # NOAA MUR SST returns temperature in Kelvin (~300 K).
        # Convert to Celsius if value is > 200:
        if val is not None and val > 200:
            val = round(val - 273.15, 2)

        return val

    except Exception:
        pass

    return None


def extract_marine_values(marine_data):
    """
    Extract SST and chlorophyll values from get_marine_data().

    Returns:
        (temperature, chlorophyll)
    """
    temperature = None
    chlorophyll = None

    try:
        sst_result = marine_data.get("sst", {})
        temperature = extract_value(sst_result)
    except Exception:
        temperature = None

    try:
        chl_result = marine_data.get("chlorophyll", {})
        chlorophyll = extract_value(chl_result)
    except Exception:
        chlorophyll = None

    return temperature, chlorophyll


# ============================================================
# SINGLE LOCATION MARINE DATA (PARALLEL FETCH)
# ============================================================

def get_marine_data(lat, lon, date):
    """
    Fetch SST and chlorophyll for one location in parallel.
    """
    def fetch_sst():
        return get_sst(lat, lon, date)

    def fetch_chl():
        return get_chlorophyll(lat, lon, date)

    with ThreadPoolExecutor(max_workers=2) as executor:
        f_sst = executor.submit(fetch_sst)
        f_chl = executor.submit(fetch_chl)
        sst = f_sst.result()
        chlorophyll = f_chl.result()

    return {
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "date": date,
        "chlorophyll": chlorophyll,
        "sst": sst
    }


# ============================================================
# EXTRACT ERDDAP TABLE
# ============================================================

def extract_rows(result):
    """
    Extract rows from an ERDDAP JSON response.
    """
    try:
        return result["table"]["rows"]
    except Exception:
        return []


# ============================================================
# SPATIAL SST REQUEST
# ============================================================

def get_spatial_sst(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    date,
    step=0.2
):
    """
    Fetch an entire SST grid using ONE ERDDAP request.
    """
    query = (
        f"?analysed_sst"
        f"[({date}T00:00:00Z)]"
        f"[({min_lat}):{step}:({max_lat})]"
        f"[({min_lon}):{step}:({max_lon})]"
    )

    try:
        response = requests.get(
            NOAA_SST_URL + query,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("NOAA spatial SST error:", e)
        return {
            "error": str(e)
        }


# ============================================================
# SPATIAL CHLOROPHYLL REQUEST
# ============================================================

def get_spatial_chlorophyll(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    date,
    step=0.2
):
    """
    Fetch an entire chlorophyll grid using ONE ERDDAP request.
    """
    query = (
        f"?CHL"
        f"[({date}T00:00:00Z)]"
        f"[({min_lat}):{step}:({max_lat})]"
        f"[({min_lon}):{step}:({max_lon})]"
    )

    try:
        response = requests.get(
            INCOIS_CHL_URL + query,
            timeout=REQUEST_TIMEOUT,
            verify=False
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("INCOIS spatial chlorophyll error:", e)
        return {
            "error": str(e)
        }


# ============================================================
# BUILD SPATIAL GRID
# ============================================================

def build_grid(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    step
):
    """
    Create the expected spatial grid.
    """
    locations = []
    lat = min_lat

    while lat <= max_lat + 0.00001:
        lon = min_lon

        while lon <= max_lon + 0.00001:
            locations.append(
                {
                    "latitude": round(lat, 4),
                    "longitude": round(lon, 4)
                }
            )
            lon += step

        lat += step

    return locations


# ============================================================
# FAST SPATIAL MARINE DATA
# ============================================================

def get_spatial_marine_data(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    date,
    step=0.2
):
    sst_data = get_spatial_sst(
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        date,
        step
    )

    chl_data = get_spatial_chlorophyll(
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        date,
        step
    )

    grid = build_grid(
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        step
    )

    # --------------------------------------------------------
    # Parse SST
    # --------------------------------------------------------
    sst_rows = extract_rows(sst_data)
    sst_values = {}

    for row in sst_rows:
        try:
            latitude = safe_float(row[1])
            longitude = safe_float(row[2])
            temperature = safe_float(row[3])

            if temperature is not None and temperature > 200:
                temperature = round(temperature - 273.15, 2)

            if latitude is not None and longitude is not None:
                key = (
                    round(latitude, 4),
                    round(longitude, 4)
                )
                sst_values[key] = temperature

        except Exception:
            continue

    # --------------------------------------------------------
    # Parse Chlorophyll
    # --------------------------------------------------------
    chl_rows = extract_rows(chl_data)
    chl_values = {}

    for row in chl_rows:
        try:
            latitude = safe_float(row[1])
            longitude = safe_float(row[2])
            chlorophyll = safe_float(row[3])

            if latitude is not None and longitude is not None:
                key = (
                    round(latitude, 4),
                    round(longitude, 4)
                )
                chl_values[key] = chlorophyll

        except Exception:
            continue

    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------
    locations = []

    for point in grid:
        latitude = point["latitude"]
        longitude = point["longitude"]
        key = (latitude, longitude)

        locations.append(
            {
                "latitude": latitude,
                "longitude": longitude,
                "temperature": sst_values.get(key),
                "chlorophyll": chl_values.get(key),
                "sst_source": "NOAA CoastWatch",
                "chlorophyll_source": "INCOIS",
                "date": date
            }
        )

    valid_sst = sum(
        1 for loc in locations if loc["temperature"] is not None
    )
    valid_chl = sum(
        1 for loc in locations if loc["chlorophyll"] is not None
    )
    valid_both = sum(
        1 for loc in locations
        if loc["temperature"] is not None and loc["chlorophyll"] is not None
    )

    return {
        "source": [
            "NOAA CoastWatch",
            "INCOIS"
        ],
        "date": date,
        "bounds": {
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_lon": min_lon,
            "max_lon": max_lon
        },
        "grid_step": step,
        "total_locations": len(locations),
        "valid_sst_locations": valid_sst,
        "valid_chlorophyll_locations": valid_chl,
        "valid_combined_locations": valid_both,
        "locations": locations
    }

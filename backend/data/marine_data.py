import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

NOAA_SST_URL = (
    "https://coastwatch.pfeg.noaa.gov/erddap/"
    "griddap/jplMURSST41.json"
)

INCOIS_CHL_URL = (
    "https://erddap.incois.gov.in/erddap/griddap/"
    "incois_oceansat2_datasets.json"
)

REQUEST_TIMEOUT = 30


def safe_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def get_sst(lat, lon, date):
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

        if response.ok:
            data = response.json()

            rows = (
                data
                .get("table", {})
                .get("rows", [])
            )

            if rows:
                return {
                    "source": "NOAA CoastWatch",
                    "variable": "sea_surface_temperature",
                    "latitude": lat,
                    "longitude": lon,
                    "date": rows[0][0],
                    "value": rows[0][-1],
                    "data": data
                }

        print(
            "Requested NOAA SST date unavailable. "
            "Trying latest available SST."
        )

    except Exception as noaa_error:
        print(
            "NOAA requested-date SST failed:",
            noaa_error
        )

    # Get the latest available SST observation
    try:
        latest_query = (
            f"?analysed_sst"
            f"[({date}T00:00:00Z):1]"
            f"[({lat})]"
            f"[({lon})]"
        )

        response = requests.get(
            NOAA_SST_URL + latest_query,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        rows = (
            data
            .get("table", {})
            .get("rows", [])
        )

        if rows:
            return {
                "source": "NOAA CoastWatch",
                "variable": "sea_surface_temperature",
                "latitude": lat,
                "longitude": lon,
                "date": rows[-1][0],
                "value": rows[-1][-1],
                "data": data,
                "fallback": True
            }

    except Exception as latest_error:
        print(
            "NOAA latest SST failed:",
            latest_error
        )

    # Open-Meteo fallback
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

        temperature = (
            data
            .get("current", {})
            .get("sea_surface_temperature")
        )

        return {
            "source": "Open-Meteo Marine",
            "variable": "sea_surface_temperature",
            "latitude": lat,
            "longitude": lon,
            "date": data.get(
                "current", {}
            ).get(
                "time",
                date
            ),
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
            "error": str(fallback_error)
        }

def get_chlorophyll(lat, lon, date):
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


def extract_value(result):
    try:
        if not isinstance(result, dict):
            return None

        value = result.get("value")

        if value is not None:
            value = safe_float(value)

            if value is not None and value > 200:
                value -= 273.15

            return round(value, 2) if value is not None else None

        rows = (
            result
            .get("data", {})
            .get("table", {})
            .get("rows", [])
        )

        if rows:
            value = safe_float(rows[0][-1])

            if value is not None and value > 200:
                value -= 273.15

            return round(value, 2) if value is not None else None

    except Exception:
        pass

    return None


def extract_marine_values(marine_data):
    temperature = extract_value(
        marine_data.get("sst", {})
    )

    chlorophyll = extract_value(
        marine_data.get("chlorophyll", {})
    )

    return temperature, chlorophyll


def get_marine_data(lat, lon, date):

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


def extract_rows(result):
    try:
        return result["table"]["rows"]
    except Exception:
        return []


def get_spatial_sst(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    date,
    step=0.2
):
    query = (
        f"?analysed_sst"
        f"[({date}T00:00:00Z)]"
        f"[({min_lat}):{step}:({max_lat})]"
        f"[({min_lon}):{step}:({max_lon})]"
    )

    try:
        response = requests.get(
            NOAA_SST_URL + query,
            timeout=8
        )

        response.raise_for_status()

        data = response.json()

        if data.get("table", {}).get("rows", []):
            return data

    except Exception as e:
        print(
            "NOAA spatial SST unavailable:",
            e
        )

    rows = []

    latitudes = []
    longitudes = []

    lat = min_lat

    while lat <= max_lat + 0.0001:
        latitudes.append(round(lat, 4))
        lat += step

    lon = min_lon

    while lon <= max_lon + 0.0001:
        longitudes.append(round(lon, 4))
        lon += step

    def fetch_point(point_lat, point_lon):
        try:
            response = requests.get(
                "https://marine-api.open-meteo.com/v1/marine",
                params={
                    "latitude": point_lat,
                    "longitude": point_lon,
                    "current": "sea_surface_temperature"
                },
                timeout=8
            )

            response.raise_for_status()

            data = response.json()

            temperature = (
                data
                .get("current", {})
                .get("sea_surface_temperature")
            )

            if temperature is not None:
                return [
                    data.get("current", {}).get("time"),
                    point_lat,
                    point_lon,
                    temperature
                ]

        except Exception as e:
            print(
                f"Open-Meteo SST failed "
                f"({point_lat},{point_lon}): {e}"
            )

        return None

    points = [
        (point_lat, point_lon)
        for point_lat in latitudes
        for point_lon in longitudes
    ]

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(
            lambda p: fetch_point(p[0], p[1]),
            points
        )

        for result in results:
            if result is not None:
                rows.append(result)

    if rows:
        print(
            f"Using Open-Meteo Marine SST fallback: "
            f"{len(rows)} points"
        )

        return {
            "table": {
                "columnNames": [
                    "time",
                    "latitude",
                    "longitude",
                    "sea_surface_temperature"
                ],
                "rows": rows
            },
            "source": "Open-Meteo Marine"
        }

    return {
        "table": {
            "rows": []
        },
        "error": (
            "SST data unavailable "
            "from NOAA and Open-Meteo"
        )
    }


def get_spatial_chlorophyll(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    date,
    step=0.2
):
    query = (
        f"?CHL"
        f"[({date}T00:00:00Z)]"
        f"[({min_lat}):{step}:({max_lat})]"
        f"[({min_lon}):{step}:({max_lon})]"
    )

    try:
        response = requests.get(
            INCOIS_CHL_URL + query,
            timeout=15,
            verify=False
        )

        response.raise_for_status()

        data = response.json()

        if data.get("table", {}).get("rows", []):
            return data

    except Exception as e:
        print(
            "INCOIS spatial chlorophyll unavailable:",
            e
        )

    return {
        "table": {
            "columnNames": [
                "time",
                "latitude",
                "longitude",
                "chlorophyll"
            ],
            "rows": []
        },
        "source": "INCOIS"
    }


def build_grid(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    step=0.2
):
    latitudes = []
    longitudes = []

    lat = min_lat

    while lat <= max_lat + 0.0001:
        latitudes.append(round(lat, 4))
        lat += step

    lon = min_lon

    while lon <= max_lon + 0.0001:
        longitudes.append(round(lon, 4))
        lon += step

    return latitudes, longitudes


def get_spatial_marine_data(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    date,
    step=0.2
):
    sst = get_spatial_sst(
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        date,
        step
    )

    chlorophyll = get_spatial_chlorophyll(
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        date,
        step
    )

    return {
        "bounds": {
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_lon": min_lon,
            "max_lon": max_lon
        },
        "date": date,
        "sst": sst,
        "chlorophyll": chlorophyll
    }
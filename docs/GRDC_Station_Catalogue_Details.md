# GRDC Station Catalogue — Full Details

> This document records all known GRDC station metadata fields, data sources, download methods, and API endpoints discovered during reverse engineering.

---

## 1. Station Metadata Columns

### 1.1 Columns Available in the Portal (Data Download → Stations, Filter: ALL)

The GRDC Data Portal exposes the following columns when downloading the full station list:

| # | Portal Column Name | Chinese | Description |
|---|---|---|---|
| 1 | **Station Number** | 站点编号 | GRDC unique identifier (numeric) |
| 2 | **Station Name** | 站点名称 | Official gauging station name |
| 3 | **Region** | 区域 | WMO region code |
| 4 | **Sub-region** | 子区域 | WMO sub-region code |
| 5 | **National ID** | 国家编号 | National gauging station identifier |
| 6 | **River Name** | 河流名称 | River or watercourse name |
| 7 | **Country** | 国家 | ISO 3166-1 alpha-3 country code |
| 8 | **Latitude** | 纬度 | Station latitude (decimal degrees, WGS84) |
| 9 | **Longitude** | 经度 | Station longitude (decimal degrees, WGS84) |
| 10 | **Area (km²)** | 流域面积 | Catchment area reported by data provider (km²) |
| 11 | **Altitude (m)** | 海拔 | Station altitude above sea level (m) |
| 12 | **Downstream Station Number** | 下游站点编号 | GRDC number of the downstream station |
| 13 | **Daily Start** | 日数据起始 | First date of daily discharge data |
| 14 | **Daily End** | 日数据结束 | Last date of daily discharge data |
| 15 | **Daily Years** | 日数据年数 | Number of years with daily data |
| 16 | **Daily Missing (%)** | 日数据缺失率 | Percentage of missing daily values |
| 17 | **Monthly Start** | 月数据起始 | First date of monthly discharge data |
| 18 | **Monthly End** | 月数据结束 | Last date of monthly discharge data |
| 19 | **Monthly Years** | 月数据年数 | Number of years with monthly data |
| 20 | **Monthly Missing (%)** | 月数据缺失率 | Percentage of missing monthly values |
| 21 | **Earliest Data** | 最早数据 | Earliest available data date |
| 22 | **Latest Data** | 最晚数据 | Latest available data date |
| 23 | **Maximum Data Length** | 最大数据长度 | Maximum record length (years) |
| 24 | **Long-term Mean Discharge (m³/s)** | 长期平均流量 | Mean discharge over full record (m³/s) |
| 25 | **Mean Annual Volume (km³)** | 年均径流量 | Mean annual water volume (km³) |
| 26 | **Mean Annual Runoff Depth (mm)** | 年均径流深 | Mean annual runoff depth (mm) |

### 1.2 Columns Available in the Watershed Shapefile

The `GRDC_Watersheds_shp.zip` (extracted as timestamp-named `.shp`) contains:

| # | Field Name | Type | Description |
|---|---|---|---|
| 1 | `grdc_no` | N | GRDC station number (key field) |
| 2 | `river` | C (80) | River name |
| 3 | `station` | C (80) | Station name |
| 4 | `area` | N | Reported catchment area (km²) |
| 5 | `altitude` | N | Station altitude (m) |
| 6 | `lat_org` | N | Original station latitude |
| 7 | `long_org` | N | Original station longitude |
| 8 | `lat_pp` | N | Pour point latitude (derived) |
| 9 | `long_pp` | N | Pour point longitude (derived) |
| 10 | `dist_km` | N | Distance between station and pour point (km) |
| 11 | `area_calc` | N | Calculated catchment area (km²) |
| 12 | `quality` | C (80) | Quality flag: High / Medium / Low |
| 13 | `type` | C (80) | Derivation method: Automatic / Manual |
| 14 | `comment` | C (80) | Quality description |
| 15 | `source` | C (80) | DEM source: hydrosheds / merit |
| 16 | `geometry` | Polygon | Catchment boundary polygon |

- **Total stations**: 11,267
- **CRS**: EPSG:4326 (WGS 84)
- **Coverage**: Global (lon: -163.73° to 178.30°, lat: -50.79° to 80.67°)

### 1.3 Mapping: Portal Columns → Shapefile Fields

| Portal Column | Shapefile Field | Notes |
|---|---|---|
| Station Number | `grdc_no` | ✓ Direct match |
| Station Name | `station` | ✓ Direct match |
| River Name | `river` | ✓ Direct match |
| Latitude | `lat_org` | ✓ Direct match |
| Longitude | `long_org` | ✓ Direct match |
| Area (km²) | `area` | ✓ Direct match |
| Altitude (m) | `altitude` | ✓ Direct match |
| **Region** | — | ✗ Portal only |
| **Sub-region** | — | ✗ Portal only |
| **National ID** | — | ✗ Portal only |
| **Country** | — | ✗ Portal only (infer from coords) |
| **Downstream Station Number** | — | ✗ Portal only |
| **Daily/Monthly stats** | — | ✗ Portal only |
| **Mean Discharge / Volume / Runoff** | — | ✗ Portal only |

**Conclusion**: The Shapefile covers ~60% of the Portal columns. For the remaining fields (Region, Country, data availability stats, discharge statistics), you must download from the Portal.

---

## 2. Data Sources & Download Methods

### 2.1 Static File Downloads (No Auth Required)

All URLs verified 2026-05-10, require GET request (HEAD returns 400).

| File | Format | Size | URL |
|---|---|---|---|
| Watershed Boundaries | Shapefile (.zip) | ~112 MB | `https://grdc.bafg.de/downloads/GRDC_Watersheds_shp.zip` |
| Watershed Boundaries | GeoJSON (.zip) | ~110 MB | `https://grdc.bafg.de/downloads/GRDC_Watersheds_geojson.zip` |
| Major River Basins | Shapefile (.zip) | — | `https://grdc.bafg.de/downloads/GRDC_Major_River_Basins.zip` |
| WMO Basins & Sub-basins | Shapefile (.zip) | — | `https://grdc.bafg.de/downloads/GRDC_WMO_Basins.zip` |

### 2.2 Station Catalogue (Extracted from Shapefile)

This repo includes `GRDC_Station_Catalogue.csv` extracted from the Shapefile:

```
GRDC_Station_Catalogue.csv   (11,267 records, 15 fields)
```

### 2.3 Full Station Catalogue (Portal Only)

The complete 26-column station catalogue **can only be obtained from the GRDC Data Portal** via its web UI.

**Portal URL**: https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser

**Steps**:
1. Open the URL above (no login required, uses PublicUser)
2. Wait for the SPA to load
3. Navigate: left sidebar → **Data Download** → **Stations**
4. Set all filters to **ALL** (to get the full catalogue)
5. Click the **download/export** button → CSV file

> **Note**: The portal's download button can be hard to find. It appears as an icon in the toolbar above the station table. Look for a download/export icon (often a floppy disk or arrow icon).

---

## 3. GRDC Portal API Reference (Reverse Engineered)

### 3.1 Portal Architecture

| Component | Detail |
|---|---|
| Frontend | Dojo Toolkit (JavaScript SPA) |
| Backend | Apache Tomcat |
| API Base | `https://portal.grdc.bafg.de/KiWebPortal/rest/` |
| Auth | Session-based (POST `/rest/auth/login`) |
| Public Access | SPA URL param `?publicuser=PublicUser` (no API access) |

### 3.2 Discovered REST Endpoints

All endpoints require authentication (return 401 without valid session):

| Endpoint | Method | Status | Description |
|---|---|---|---|
| `/KiWebPortal/rest/packages` | GET | 401 | List installed packages |
| `/KiWebPortal/rest/users` | GET | 401 | User management |
| `/KiWebPortal/rest/users/auth` | GET | 401 | Auth status check |
| `/KiWebPortal/rest/users/current` | GET | 401 | Current user info |
| `/KiWebPortal/rest/auth/login` | POST | 405→401 | Login (expects JSON body) |

### 3.3 Login API

```
POST https://portal.grdc.bafg.de/KiWebPortal/rest/auth/login
Content-Type: application/json

{
  "userName": "<username>",
  "password": "<password>"
}
```

Response on failure:
```json
{"type":"error","status":401,"errorCode":40102,"message":"Invalid credentials."}
```

Response on missing fields:
```json
{"type":"error","status":400,"errorCode":40004,"message":"JSON document has invalid or missing data.",
 "details":[{"constraintType":"UserNameOrEmailNotNullValidation","key":"username or email","message":"one of userName or email must be specified"}]}
```

> The PublicUser account does not have a known password for API access. The portal's public mode (`?publicuser=PublicUser`) is JavaScript-level only and does not grant REST API session.

### 3.4 Failed Endpoint Probes (All 404)

These URLs were tested and confirmed non-existent:

```
https://portal.grdc.bafg.de/api/stations
https://portal.grdc.bafg.de/rest/stations
https://portal.grdc.bafg.de/rest/datasets
https://portal.grdc.bafg.de/rest/datasources
https://portal.grdc.bafg.de/kml/grdc_stations.kml
https://portal.grdc.bafg.de/geoserver/wfs?...
https://grdc.bafg.de/downloads/GRDC_Stations.csv
https://grdc.bafg.de/downloads/grdc_stations.kml
https://grdc.bafg.de/downloads/GRDC_Stations.geojson
```

---

## 4. Shapefile Field Definitions (Detailed)

### 4.1 Quality Field Values

| Value | Meaning |
|---|---|
| `High` | Area difference ≤ 5% and distance ≤ 5 km |
| `Medium` | Area difference 5–10% and distance ≤ 5 km |
| `Low` | Area difference 10–50% and distance ≤ 5 km |

### 4.2 Type Field Values

| Value | Meaning |
|---|---|
| `Automatic` | Derived automatically from DEM using flow direction model |
| `Manual` | Adjusted manually (e.g., station location correction) |

### 4.3 Source Field Values

| Value | Meaning |
|---|---|
| `hydrosheds` | Based on HydroSHEDS 15s DEM (Lehner et al., 2008) |
| `merit` | Based on MERIT Hydro DEM (Yamazaki et al., 2019) |

### 4.4 Comment Field Examples

```
"Area difference <= 5% and distance <= 5 km"
"Area difference 5-10% and distance <= 5 km"
"Area difference 10-50% and distance <= 5 km"
"Location seems correct, but GRDC area seems wrong"
```

---

## 5. Citation

```
GRDC (2023): Watershed Boundaries of GRDC Stations.
Global Runoff Data Centre. Koblenz, Germany:
Federal Institute of Hydrology (BfG).
```

Reference:
- Lehner, B., Verdin, K., Jarvis, A. (2008): New global hydrography derived from spaceborne elevation data. *Eos, Transactions, AGU*, 89(10): 93-94.
- GRDC Report Series No. 41 (2012): Algorithm Theoretical Basis Document — Catchment boundaries of GRDC gauging stations.

---

## 6. Update Log

| Date | Content |
|---|---|
| 2026-05-10 | Initial version: field definitions, download URLs, API probe results |
| 2026-05-10 | Extracted `GRDC_Station_Catalogue.csv` (11,267 records) from Shapefile |

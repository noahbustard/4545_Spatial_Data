# WDO Field Manual — Core Geometry + Sanity Checks
World Defense Organization (WDO) — Missile Geometry 101

> Your job is not to fire weapons.  
> Your job is to **trust geometry**.  
> If you can see it, you can trust it.  
> (If you can’t see it, it’s probably wrong.)  

---

## 0) Coordinate Rules (Non-Negotiable)

- **Latitude**: north/south (−90 to +90)
- **Longitude**: east/west (−180 to +180)
- In GeoJSON coordinates are typically **[lon, lat]** (x then y).
- In most “math functions” we pass **(lat, lon)** because humans like pain.

**Unit trap**:
- Degrees are **not** meters.
- If you buffer polygons in degrees and call it “100km,” you are doing fantasy cartography.

---

## 1) Haversine Distance (Great-Circle Distance)

### What it is
Distance along the surface of a sphere (Earth-ish).

### Inputs/Outputs
- Input: (lat1, lon1, lat2, lon2) in **degrees**
- Output: **kilometers** (km)

### Formula (conceptual)
1) Convert degrees → radians  
2) Compute spherical angular distance  
3) Multiply by Earth radius

### Sanity checks
- Same point → 0 km
- ~1 degree of latitude ≈ **111 km**
- If your “nearby city” distance is 12,000 km, your code is lying.

---

## 2) Initial Bearing (Forward Azimuth)

### What it is
The compass direction you must start traveling from point A to reach point B
(along a great-circle path).

### Inputs/Outputs
- Input: (lat1, lon1, lat2, lon2) in degrees
- Output: bearing in degrees, normalized to **0–360**

### Sanity checks
- Bearing is **direction**, not slope.
- A bearing near:
  - 0° ≈ north-ish
  - 90° ≈ east-ish
  - 180° ≈ south-ish
  - 270° ≈ west-ish

---

## 3) Destination Point (Given Start + Bearing + Distance)

### What it is
Where you end up if you travel `distance_km` from (lat, lon) along `bearing_deg`.

### Inputs/Outputs
- Input: start (lat, lon) in degrees, bearing in degrees, distance in km
- Output: destination (lat, lon) in degrees

### Sanity checks
- Distance = 0 → same point
- Bearings behave like a compass (0 north, 90 east)
- Near poles and the dateline, weird things happen. That’s not a bug. That’s Earth.

---

## 4) Trajectories: Point → Line

### What it is
A “threat path” is a **sequence of points** turned into a line geometry.

### Minimal workflow
- Start point
- Compute destination after some time / distance
- Create intermediate points (for visualization)
- Build a LineString from them (library geometry)

### Sanity checks
- A trajectory should “look like” its bearing on a world map
- If it curves strangely, you might be:
  - mixing CRS
  - using linear interpolation in lat/lon
  - or just learning that projection distortion is a thing

---

## 5) Buffers (aka Damage Zones)

### What it is
A buffer is “everything within X distance” of a geometry.

### **CRITICAL WARNING**
- Buffering correctly requires a projected CRS (meters).
- If you buffer in lat/lon degrees, it’s *not* a real distance buffer.

### Sanity checks
- Buffer around a point should look “round-ish”
- Buffer around a line should look like a capsule / sausage (technical term)

---

## 6) Validation Rules (How WDO Trusts Results)

- Always print key numbers:
  - distances (km)
  - bearings (deg)
  - time steps
- Always visualize:
  - points + lines + polygons
- If math and map disagree:
  - assume the code is wrong
  - then assume your CRS is wrong
  - then assume your assumptions are wrong
  - only then blame aliens

---

## 7) Allowed Black Boxes (Course Policy)

Allowed freely:
- GeoPandas: reading files, filtering, `to_crs`
- Shapely: `intersects`, `within`, `distance`, `buffer` (after CRS sanity)
- Folium: all visualization

You must implement at least once (WDO toolkit):
- Haversine distance
- Initial bearing
- Destination point

Optional (advanced / later):
- True geodesic interpolation (pyproj / GeographicLib)
- Spatial indexing (R-tree)
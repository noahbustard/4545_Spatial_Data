```yaml
id: folium_functions_worldle_contingency_2026-03-04
date: 2026-03-04
timezone: America/Chicago
topic: spatial-data-mapping
tags:
  - python
  - folium
  - leaflet
  - geojson
  - visualization
  - gameplay
  - worldle
deliverable:
  - folium_function_catalog
  - missile_101_visualization_ideas
  - worldle_game_explainer
tone: casual-borderline-sarcastic
```

Alright Terry — yes, I can help, and yes, Folium is a *very* reasonable “don’t make me write custom JavaScript” line in the sand.

Below is a **student-friendly “Folium moveset”**: functions/classes you can teach that (1) make interactive maps, and (2) **visualize the spatial math outputs** your Missile_101 problems generate (distance, bearing, intercepts, threat rings, paths, etc.). Then I’ll give you a Missile_101 “gameplay-ish” plan that stays inside the Folium sandbox (no JS rabbit holes). Finally: **Worldle** is real, and your spelling anxiety is justified because Wordle ate the internet.

---

## Folium “Moveset” for Spatial Math Visuals

### 0) The core loop (the thing students should memorize)
These are the “always” functions.

- `folium.Map(...)`  
  Create the map canvas (center, zoom, tiles).  [oai_citation:0‡Bokeh](https://python-visualization.github.io/folium/latest/reference.html?utm_source=chatgpt.com)  
- `m.save("map.html")`  
  Export to an HTML file students can open/share. (The whole point.)

**Tiny pattern:**
```python
import folium

m = folium.Map(location=[33.87, -98.52], zoom_start=13, tiles="OpenStreetMap")
m.save("out.html")
```

---

## 1) Put stuff on the map (points, icons, “here’s the thing”)

### Markers (points of interest / answers / guessed locations)
- `folium.Marker(location=[lat, lon], popup="...", tooltip="...")`
- `folium.Icon(color="red", icon="info-sign")` (classic)

Use for: target cities, launch sites, intercept points, student guesses.

### Circles (distance math made visible)
- `folium.Circle(...)` → radius **in meters** (great for “blast radius”, “safe zone”, “coverage ring”)  
- `folium.CircleMarker(...)` → fixed pixel radius (great for “just mark it, don’t scale”)

This distinction is *money* pedagogically: **Circle = real world radius**, **CircleMarker = screen dot**.  [oai_citation:1‡Data 8](https://data8.org/datascience/maps.html?utm_source=chatgpt.com)

**Example: “show a 25 km threat radius”**
```python
folium.Circle(
    location=[lat, lon],
    radius=25_000,   # meters
    popup="Threat radius: 25km"
).add_to(m)
```

---

## 2) Draw the math (lines, paths, bearings, routes)

### Lines (connect two points, show travel)
- `folium.PolyLine(locations=[(lat1, lon1), (lat2, lon2), ...], tooltip="...")`

Use for: missile path, intercept path, “guess → target” line (Worldle-style clue), patrol routes, etc.

**Example: “missile flight segment”**
```python
folium.PolyLine(
    [(lat1, lon1), (lat2, lon2)],
    tooltip="Missile path"
).add_to(m)
```

### “Direction” visualization trick (without fancy arrows)
Folium doesn’t make arrowheads painless, so do this instead:
- Draw a `PolyLine`
- Add a `Marker` at the end point labeled “→” or “END”
- (Optional) add small “breadcrumb” markers along the line

It’s not NASA, but students immediately get it.

---

## 3) GeoJSON layers (because your whole course is basically “GeoJSON: The Reckoning”)

### Load and display GeoJSON
- `folium.GeoJson(geojson_data, ...)`
- `folium.GeoJsonTooltip(fields=[...])`
- `folium.GeoJsonPopup(fields=[...])`

Use for: country outlines, danger zones, bounding boxes, campus buildings, etc.  
This is the big bridge between “math answer” and “map artifact.”  [oai_citation:2‡Bokeh](https://python-visualization.github.io/folium/latest/reference.html?utm_source=chatgpt.com)

**Example:**
```python
folium.GeoJson(
    data,
    tooltip=folium.GeoJsonTooltip(fields=["Name"])
).add_to(m)
```

---

## 4) Layer control (turn stuff on/off like a civilized person)

### Feature groups + layers
- `folium.FeatureGroup(name="Threats")`
- `folium.TileLayer("CartoDB Positron")` (or other tiles)
- `folium.LayerControl()`

Teach this early because once they have **multiple** rings/lines/guesses, the map turns into spaghetti.

**Pattern:**
```python
threats = folium.FeatureGroup(name="Threat rings").add_to(m)
paths   = folium.FeatureGroup(name="Paths").add_to(m)

# add circles/lines to threats/paths groups...
folium.LayerControl().add_to(m)
```

---

## 5) Choropleths (optional, but great for “heat” scoring)

- `folium.Choropleth(...)`  [oai_citation:3‡Programming Historian](https://programminghistorian.org/en/lessons/choropleth-maps-python-folium?utm_source=chatgpt.com)

Use for: “risk by region”, “probability surface” (even if it’s fake), “impact score by country/state/county”.

This is where you can turn Missile_101 into “strategic map mode” instead of only drawing lines.

---

## 6) Plugins (aka “the fun button”)

These live in: `from folium import plugins` (students don’t need to know Leaflet, just that plugins exist).

High-value plugins for your use-case:
- `plugins.MarkerCluster()`  
  If you have lots of points (threats, events, guesses).
- `plugins.HeatMap(data)`  
  For “density” plots (impacts, sightings, whatever).
- `plugins.MeasureControl()`  
  Lets students measure distances manually (great for sanity checks).
- `plugins.MousePosition()`  
  Shows live lat/lon under the cursor (instant feedback).
- `plugins.MiniMap()`  
  Makes it feel “game-y” with almost zero effort.

(These are all standard Folium patterns; the official reference lists plugins and core objects.  [oai_citation:4‡Bokeh](https://python-visualization.github.io/folium/latest/reference.html?utm_source=chatgpt.com))

---

## 7) Output patterns that feel like “gameplay” (still no JS spelunking)

If you want “turn-based” vibes:
1. Generate a map per step: `turn_01.html`, `turn_02.html`, …
2. Or generate one map with LayerControl and group each turn as a layer.

That’s basically “replay mode” without writing an engine.

---

# Missile_101: “Gameplay” Without Writing a Game Engine

Here are **3 escalating tiers** that stay Folium-native:

## Tier A: Tactical Overlay (fast, effective)
- Base map + launch sites + targets
- Rings for ranges (threat, defense, radar)
- Lines for trajectories
- Popups show computed values:
  - distance
  - bearing
  - ETA (even if simplified)
  - intercept feasibility

Students “see” their math.

## Tier B: Turn-based Guess/Intercept (Worldle-adjacent)
Each “turn”:
- Student chooses an intercept point (or defense site)
- You compute:
  - distance to missile path
  - time-to-intercept window
  - success/fail score
- Map shows:
  - their guess marker
  - the closest approach point on the path
  - a ring representing “intercept radius”
  - a line from guess → closest approach

Export one HTML per turn. It feels like a game replay.

## Tier C: Scenario generator + scoreboard (still simple)
- Randomized threats (seeded)
- Score based on:
  - how quickly they respond
  - how close their intercept is
  - how many “assets” remain safe
- Final output:
  - map.html
  - summary.json (or csv)
  - maybe a tiny leaderboard table

No JS. No browser framework. Just “math + maps + receipts.”

---

# Worldle: yes, it’s a thing

You mean **Worldle** (with an “l”) — a daily geography guessing game where you identify a country/territory from its **silhouette**, and after wrong guesses it gives **distance and direction clues**.  [oai_citation:5‡Worldle](https://worldle.teuteuf.fr/?utm_source=chatgpt.com)

That mechanic is *perfect* for your contingency plan because it’s basically:
- pick a target geometry
- student makes a guess
- compute:
  - distance (haversine)
  - bearing (direction)
- visualize:
  - guess marker
  - target outline
  - line guess→target
  - popup with distance + bearing

In other words: **your spatial math curriculum wearing a trench coat pretending to be a game.**

---

## If you want, here’s a clean “student checklist” for Folium labs
1. Start map (`folium.Map`)
2. Add basemap choices (`TileLayer`)
3. Add points (`Marker`, `CircleMarker`)
4. Add real-world rings (`Circle`)
5. Add lines (`PolyLine`)
6. Add GeoJSON (`GeoJson + Tooltip/Popup`)
7. Organize layers (`FeatureGroup`)
8. Turn layers on/off (`LayerControl`)
9. Export (`save`)

If you want the next step, tell me what data objects your Missile_101 code already produces (just the *shape*: e.g., list of points, list of paths, per-threat radii), and I’ll turn it into a **drop-in “map_renderer.py”** with 3–4 functions your students can call like Legos.
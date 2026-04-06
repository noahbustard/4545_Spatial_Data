# Missile_Geometry_101 → WDO Mapping Table

## Suggested promotion rule

Promote notebook code into `wdo` when it is:

- reused in 2+ notebooks
- stable enough to name cleanly
- annoying enough that copy/paste now feels gross

---

## Foundation / IO / Paths

| Module | Notebook                | Main idea                    | Reusable helpers                                                              | Target module          |
| ------ | ----------------------- | ---------------------------- | ----------------------------------------------------------------------------- | ---------------------- |
| 00     | 00-Working_Directory    | cwd, listing, existence      | `cwd()`, `path_exists()`, `is_file()`, `is_dir()`                             | `wdo.io.paths`         |
| 00     | 01-Relative_vs_Absolute | safe path handling           | `abs_path()`, `resolve_path()`, `join_path()`                                 | `wdo.io.paths`         |
| 00     | 02-Data_Elsewhere       | data outside notebook folder | `project_data_path()`                                                         | `wdo.io.paths`         |
| 00     | 03-Find_Project_Root    | walk upward to root          | `find_project_root()`, `find_upwards()`                                       | `wdo.io.paths`         |
| 01     | 00-Reading_JSON         | JSON load/save               | `load_json()`, `save_json()`, `pretty_json()`                                 | `wdo.io.json_tools`    |
| 01     | 01-GeoJSON_Structure    | GeoJSON parsing              | `load_geojson()`, `is_feature()`, `is_feature_collection()`, `get_features()` | `wdo.io.geojson_tools` |
| 01     | 02-Feature_Collections  | iterate features             | `feature_count()`, `iter_features()`, `get_geometry()`, `get_properties()`    | `wdo.io.geojson_tools` |

---

## Maps / Viewing / Styling / Interaction

| Module | Notebook              | Main idea           | Reusable helpers                                                          | Target module                 |
| ------ | --------------------- | ------------------- | ------------------------------------------------------------------------- | ----------------------------- |
| 02     | 00-Geojson.io         | validation/demo     | `validate_basic_geojson()`                                                | `wdo.utils.validation`        |
| 02     | 01-iPyLeaflet_Intro   | make map            | `make_map()`, `add_basemap()`                                             | `wdo.maps.leaflet_helpers`    |
| 02     | 02-Add_GeoJSON        | add data to map     | `add_geojson()`, `fit_map_to_geojson()`                                   | `wdo.maps.leaflet_helpers`    |
| 02     | 03-Map_Control        | controls/toggles    | `add_layer_control()`, `add_scale_control()`                              | `wdo.maps.leaflet_helpers`    |
| 03     | 00-Properties         | inspect attributes  | `property_names()`, `get_property()`                                      | `wdo.io.geojson_tools`        |
| 03     | 01-Style_Functions    | style by properties | `style_constant()`, `style_by_property()`                                 | `wdo.maps.style_tools`        |
| 03     | 02-Filtering          | select subsets      | `filter_features()`, `filter_by_property()`, `filter_by_property_range()` | `wdo.spatial.feature_queries` |
| 04     | 00-Map_Events         | event basics        | `bind_click_logger()`, `capture_clicks()`                                 | `wdo.maps.interaction`        |
| 04     | 01-Click_Interactions | click → coords      | `extract_click_latlon()`, `format_click()`                                | `wdo.maps.interaction`        |
| 04     | 02-Dynamic_Layers     | replace/add layers  | `replace_layer()`                                                         | `wdo.maps.interaction`        |
| 04     | 03-User_Feedback      | popup/status        | `popup_text()`, `add_marker_with_popup()`                                 | `wdo.maps.interaction`        |

---

## Core Geometry

| Module | Notebook                 | Main idea               | Reusable helpers                                                    | Target module                                        |
| ------ | ------------------------ | ----------------------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| 05     | 00-Coordinate_Ranges     | valid lat/lon           | `valid_lat()`, `valid_lon()`, `valid_latlon()`                      | `wdo.geometry.points`                                |
| 05     | 01-Compute_BBox          | bbox generation         | `bbox_from_points()`, `bbox_from_feature()`, `bbox_from_features()` | `wdo.geometry.bbox`                                  |
| 05     | 02-Draw_BBox             | bbox visualization      | `bbox_to_polygon()`, `add_bbox()`                                   | `wdo.geometry.bbox`, `wdo.maps.leaflet_helpers`      |
| 05     | 03-Why_LatLon_Is_Weird   | degree weirdness        | `lon_degree_length_at_lat()`, `lat_degree_length()`                 | `wdo.geometry.points`                                |
| 06     | 00-Euclidean_Distance    | planar distance         | `euclidean()`                                                       | `wdo.geometry.distance`                              |
| 06     | 01-Haversine_Distance    | spherical distance      | `haversine_km()`, `haversine_miles()`                               | `wdo.geometry.distance`                              |
| 06     | 02-Compare_Methods       | compare distance models | `compare_distance_methods()`                                        | `wdo.geometry.distance`                              |
| 06     | 03-Distance_Applications | nearest/thresholds      | `distance_to_feature()`, `nearest_feature()`                        | `wdo.geometry.distance`                              |
| 06     | 04-Performance_Batching  | repeated computations   | `distances_from_point()`, `pairwise_distances()`                    | `wdo.geometry.distance`                              |
| 07     | 00-What_Is_Bearing       | bearing basics          | `normalize_bearing()`, `bearing_to_compass()`                       | `wdo.geometry.bearing`                               |
| 07     | 01-Compute_Bearing       | actual bearing          | `initial_bearing()`                                                 | `wdo.geometry.bearing`                               |
| 07     | 02-Bearing_V_Direction   | text direction          | `direction_label()`                                                 | `wdo.geometry.bearing`                               |
| 07     | 03-Bearing_Applications  | move from point         | `destination_point()`, `interpolate_path()`                         | `wdo.geometry.bearing`, `wdo.geometry.interpolation` |
| 07     | 04-Advanced_Bearing      | angular difference      | `bearing_difference()`                                              | `wdo.geometry.bearing`                               |

---

## Motion / Pursuit / Simulation

| Module | Notebook                       | Main idea           | Reusable helpers                                | Target module                                   |
| ------ | ------------------------------ | ------------------- | ----------------------------------------------- | ----------------------------------------------- |
| 08     | 00-Problem_Setup               | moving-object model | `make_track()`                                  | `wdo.games.pursuit`                             |
| 08     | 01-Constant_Velocity_Intercept | predict motion      | `predict_position()`, `time_to_intercept()`     | `wdo.games.pursuit`                             |
| 08     | 02-Iterative_Pursuit           | step simulation     | `simulate_pursuit_step()`, `simulate_pursuit()` | `wdo.games.pursuit`                             |
| 08     | 03-Visual_Simulation           | path display        | `track_to_linestring()`, `add_path()`           | `wdo.games.pursuit`, `wdo.maps.leaflet_helpers` |
| 08     | 04-Strategy_and_Limits         | feasibility         | `can_intercept()`                               | `wdo.games.pursuit`                             |
| 08     | 05-Advanced_Topics             | extension area      | notebook-local unless reused                    | `wdo.games.pursuit`                             |

---

## Intersections / Buffers / PIP

| Module | Notebook                             | Main idea                   | Reusable helpers                                    | Target module                 |
| ------ | ------------------------------------ | --------------------------- | --------------------------------------------------- | ----------------------------- |
| 09     | 00-Lines_as_Paths                    | lines as segments           | `path_to_segments()`                                | `wdo.spatial.intersections`   |
| 09     | 01-Line_Segment_Intersection         | segment intersection        | `segments_intersect()`, `intersection_point()`      | `wdo.spatial.intersections`   |
| 09     | 02-Line_vs_Polygon_Basics            | line-polygon relation       | `line_intersects_polygon()`                         | `wdo.spatial.intersections`   |
| 09     | 03-Detecting_Intersections           | scan many features          | `intersecting_features()`                           | `wdo.spatial.intersections`   |
| 09     | 04-Highlighting_Intersected_Features | style hits                  | `highlight_features()`                              | `wdo.maps.style_tools`        |
| 09     | 05-Applications_Missile_Paths        | first hit logic             | `first_intersection()`                              | `wdo.spatial.intersections`   |
| 10     | 00-Buffer_Concepts                   | buffer meaning              | concept only                                        | —                             |
| 10     | 01-Buffering_Points                  | point buffers               | `buffer_point()`                                    | `wdo.spatial.buffers`         |
| 10     | 02-Buffering_Lines                   | line buffers                | `buffer_line()`                                     | `wdo.spatial.buffers`         |
| 10     | 03-Comparing_Buffer_Sizes            | multiple radii              | `multi_buffer()`                                    | `wdo.spatial.buffers`         |
| 10     | 04-Buffer_Visualization_Strategies   | styled zones                | `buffer_style()`                                    | `wdo.maps.style_tools`        |
| 10     | 05-CRS_Limitations                   | warn on bad CRS assumptions | `warn_if_geographic_crs()`                          | `wdo.utils.validation`        |
| 10     | 06-Applications_Impact_Zones         | zone membership             | `features_within_buffer()`                          | `wdo.spatial.buffers`         |
| 11     | 00_Click_Capture                     | click capture               | `extract_click_latlon()`                            | `wdo.maps.interaction`        |
| 11     | 01_Point_Representation              | point structures            | `make_point()`, `point_to_lonlat()`                 | `wdo.geometry.points`         |
| 11     | 02_Point_In_Polygon_Basics           | containment                 | `point_in_polygon()`                                | `wdo.spatial.pip`             |
| 11     | 03_Ray_Casting_Algorithm             | manual algorithm            | `ray_casting()`                                     | `wdo.spatial.pip`             |
| 11     | 04_Testing_Against_Multiple_Features | multi-feature scan          | `containing_feature()`, `all_containing_features()` | `wdo.spatial.pip`             |
| 11     | 05_Region_Classification             | point → region label        | `classify_point()`                                  | `wdo.spatial.feature_queries` |
| 11     | 06_Interactive_Click_Applications    | live map classification     | combine helpers                                     | multiple                      |

---

## Refactor / Package / Later Projects

| Module | Notebook                    | Main idea              | Reusable helpers                   | Target module |
| ------ | --------------------------- | ---------------------- | ---------------------------------- | ------------- |
| 12     | 01-From-Notebook-to-Module  | refactor repeated code | no new helpers; migration notebook | all           |
| 13     | 01-Installing-and-Using-WDO | package usage          | no new helpers; packaging notebook | all           |

---

# Suggested `src/wdo` Directory Scaffold

Below is a **practical starter scaffold**. Not every function needs to be implemented now. The point is to give each idea a home before your repo turns into a junk drawer with syntax highlighting.

---

## Directory tree

```text
src/wdo/
├── __init__.py
├── io/
│   ├── __init__.py
│   ├── paths.py
│   ├── json_tools.py
│   └── geojson_tools.py
├── maps/
│   ├── __init__.py
│   ├── leaflet_helpers.py
│   ├── style_tools.py
│   └── interaction.py
├── geometry/
│   ├── __init__.py
│   ├── points.py
│   ├── bbox.py
│   ├── distance.py
│   ├── bearing.py
│   ├── interpolation.py
│   └── simplify.py
├── spatial/
│   ├── __init__.py
│   ├── feature_queries.py
│   ├── intersections.py
│   ├── buffers.py
│   └── pip.py
├── games/
│   ├── __init__.py
│   ├── worldle.py
│   └── pursuit.py
├── graphs/
│   ├── __init__.py
│   ├── rail_graph.py
│   ├── connectivity.py
│   └── routing.py
└── utils/
    ├── __init__.py
    ├── formatting.py
    └── validation.py
```

---

# Stub files

## `src/wdo/__init__.py`

```python
"""
WDO spatial helpers for Missile_Geometry_101 and follow-on projects.
"""

__all__ = [
    "io",
    "maps",
    "geometry",
    "spatial",
    "games",
    "graphs",
    "utils",
]
```

---

## `src/wdo/io/__init__.py`

```python
from .paths import *
from .json_tools import *
from .geojson_tools import *
```

## `src/wdo/io/paths.py`

```python
from pathlib import Path


def cwd() -> Path:
    """Return the current working directory."""
    return Path.cwd()


def path_exists(path) -> bool:
    """Return True if path exists."""
    return Path(path).exists()


def is_file(path) -> bool:
    """Return True if path is a file."""
    return Path(path).is_file()


def is_dir(path) -> bool:
    """Return True if path is a directory."""
    return Path(path).is_dir()


def abs_path(path) -> Path:
    """Return absolute path without necessarily resolving symlinks."""
    return Path(path).absolute()


def resolve_path(path) -> Path:
    """Return fully resolved path."""
    return Path(path).resolve()


def join_path(*parts) -> Path:
    """Join path parts safely."""
    return Path(*parts)


def find_upwards(target_name: str, start_path=".") -> Path | None:
    """Walk upward from start_path until target_name is found."""
    current = Path(start_path).resolve()
    for parent in [current, *current.parents]:
        if (parent / target_name).exists():
            return parent / target_name
    return None


def find_project_root(marker: str = ".git", start_path=".") -> Path | None:
    """Find project root by locating marker directory/file."""
    found = find_upwards(marker, start_path)
    return found.parent if found else None


def project_data_path(*parts, marker: str = ".git", start_path=".") -> Path:
    """Return a path inside the project's data folder."""
    root = find_project_root(marker=marker, start_path=start_path)
    if root is None:
        raise FileNotFoundError(f"Could not find project root using marker={marker!r}")
    return root / "data" / Path(*parts)
```

## `src/wdo/io/json_tools.py`

```python
import json
from pathlib import Path


def load_json(path):
    """Load JSON from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path, indent: int = 2) -> None:
    """Save JSON to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def pretty_json(data) -> str:
    """Return a pretty-printed JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False)
```

## `src/wdo/io/geojson_tools.py`

```python
from .json_tools import load_json


def load_geojson(path):
    """Load GeoJSON from disk."""
    return load_json(path)


def is_feature(obj) -> bool:
    """Return True if object looks like a GeoJSON Feature."""
    return isinstance(obj, dict) and obj.get("type") == "Feature"


def is_feature_collection(obj) -> bool:
    """Return True if object looks like a GeoJSON FeatureCollection."""
    return isinstance(obj, dict) and obj.get("type") == "FeatureCollection"


def get_features(data):
    """Return features from a FeatureCollection, or [] if absent."""
    return data.get("features", []) if isinstance(data, dict) else []


def iter_features(data):
    """Yield each feature from GeoJSON data."""
    yield from get_features(data)


def feature_count(data) -> int:
    """Return number of features."""
    return len(get_features(data))


def get_geometry(feature):
    """Return geometry dict from a feature."""
    return feature.get("geometry", {})


def get_properties(feature):
    """Return properties dict from a feature."""
    return feature.get("properties", {})


def property_names(data) -> list[str]:
    """Return sorted union of property keys across all features."""
    keys = set()
    for feature in get_features(data):
        keys.update(get_properties(feature).keys())
    return sorted(keys)


def get_property(feature, key, default=None):
    """Safely retrieve a single property from a feature."""
    return get_properties(feature).get(key, default)
```

---

## `src/wdo/maps/__init__.py`

```python
from .leaflet_helpers import *
from .style_tools import *
from .interaction import *
```

## `src/wdo/maps/leaflet_helpers.py`

```python
def make_map(center=(0, 0), zoom=2, **kwargs):
    """Create and return a map object.

    Implement with folium or ipyleaflet depending on course choice.
    """
    raise NotImplementedError("Implement with folium or ipyleaflet.")


def add_basemap(map_obj, name="OpenStreetMap"):
    """Add/select a basemap layer."""
    raise NotImplementedError


def add_geojson(map_obj, data, name=None, style=None):
    """Add GeoJSON data to a map."""
    raise NotImplementedError


def fit_map_to_geojson(map_obj, data):
    """Adjust map viewport to fit GeoJSON bounds."""
    raise NotImplementedError


def add_layer_control(map_obj):
    """Add layer control widget."""
    raise NotImplementedError


def add_scale_control(map_obj):
    """Add scale control widget."""
    raise NotImplementedError


def add_bbox(map_obj, bbox, **style):
    """Draw a bounding box on the map."""
    raise NotImplementedError


def add_path(map_obj, coords, **style):
    """Add a path/polyline to the map."""
    raise NotImplementedError
```

## `src/wdo/maps/style_tools.py`

```python
def style_constant(color="blue", weight=2, fill_opacity=0.4):
    """Return a constant style dictionary/callable."""
    return {
        "color": color,
        "weight": weight,
        "fillOpacity": fill_opacity,
    }


def style_by_property(key, palette=None):
    """Return a style function keyed on a feature property."""
    raise NotImplementedError


def highlight_features(data, selected_ids, color="red"):
    """Return a modified/styled data structure highlighting selected features."""
    raise NotImplementedError


def buffer_style(distance):
    """Return style for a given buffer ring."""
    raise NotImplementedError
```

## `src/wdo/maps/interaction.py`

```python
def bind_click_logger(map_obj):
    """Bind a click event that logs coordinates."""
    raise NotImplementedError


def capture_clicks(map_obj):
    """Capture click events from a map."""
    raise NotImplementedError


def extract_click_latlon(event):
    """Extract (lat, lon) from a click event structure."""
    raise NotImplementedError


def format_click(event) -> str:
    """Return a human-readable click description."""
    raise NotImplementedError


def replace_layer(map_obj, old_layer, new_layer):
    """Remove old layer and add new layer."""
    raise NotImplementedError


def popup_text(text: str):
    """Build popup content."""
    return str(text)


def add_marker_with_popup(map_obj, lat, lon, text):
    """Add marker and popup to map."""
    raise NotImplementedError
```

---

## `src/wdo/geometry/__init__.py`

```python
from .points import *
from .bbox import *
from .distance import *
from .bearing import *
from .interpolation import *
from .simplify import *
```

## `src/wdo/geometry/points.py`

```python
import math


def valid_lat(lat: float) -> bool:
    return -90.0 <= lat <= 90.0


def valid_lon(lon: float) -> bool:
    return -180.0 <= lon <= 180.0


def valid_latlon(lat: float, lon: float) -> bool:
    return valid_lat(lat) and valid_lon(lon)


def make_point(lat: float, lon: float) -> tuple[float, float]:
    """Return a simple point as (lat, lon)."""
    return (lat, lon)


def point_to_lonlat(point: tuple[float, float]) -> tuple[float, float]:
    """Convert (lat, lon) to (lon, lat)."""
    lat, lon = point
    return (lon, lat)


def lat_degree_length() -> float:
    """Approximate meters per degree latitude."""
    return 111_320.0


def lon_degree_length_at_lat(lat: float) -> float:
    """Approximate meters per degree longitude at a given latitude."""
    return 111_320.0 * math.cos(math.radians(lat))
```

## `src/wdo/geometry/bbox.py`

```python
def bbox_from_points(points):
    """Return bbox as (min_lon, min_lat, max_lon, max_lat)."""
    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    return (min(lons), min(lats), max(lons), max(lats))


def bbox_from_feature(feature):
    """Extract all coordinates from a feature and compute bbox."""
    raise NotImplementedError


def bbox_from_features(features):
    """Compute bbox across multiple features."""
    raise NotImplementedError


def bbox_to_polygon(bbox):
    """Convert bbox tuple into a closed polygon coordinate list."""
    min_lon, min_lat, max_lon, max_lat = bbox
    return [
        (min_lat, min_lon),
        (min_lat, max_lon),
        (max_lat, max_lon),
        (max_lat, min_lon),
        (min_lat, min_lon),
    ]
```

## `src/wdo/geometry/distance.py`

```python
import math


def euclidean(p1, p2) -> float:
    """Naive planar distance between (lat, lon) points."""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def haversine_km(p1, p2) -> float:
    """Great-circle distance in kilometers between (lat, lon) points."""
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c


def haversine_miles(p1, p2) -> float:
    """Great-circle distance in miles."""
    return haversine_km(p1, p2) * 0.621371


def compare_distance_methods(p1, p2):
    """Return both Euclidean and haversine results for comparison."""
    return {
        "euclidean_deg": euclidean(p1, p2),
        "haversine_km": haversine_km(p1, p2),
        "haversine_miles": haversine_miles(p1, p2),
    }


def distances_from_point(point, points):
    """Return distances from one point to many points."""
    return [haversine_km(point, p) for p in points]


def pairwise_distances(points):
    """Return pairwise distance matrix as nested lists."""
    return [[haversine_km(a, b) for b in points] for a in points]


def distance_to_feature(point, feature):
    """Distance from point to a representative point of a feature."""
    raise NotImplementedError


def nearest_feature(point, features):
    """Return nearest feature and distance."""
    raise NotImplementedError
```

## `src/wdo/geometry/bearing.py`

```python
import math


def normalize_bearing(angle: float) -> float:
    """Normalize angle to [0, 360)."""
    return angle % 360.0


def initial_bearing(p1, p2) -> float:
    """Compute initial bearing from p1 to p2, both as (lat, lon)."""
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)

    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = (
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    )
    bearing = math.degrees(math.atan2(x, y))
    return normalize_bearing(bearing)


def bearing_to_compass(angle: float) -> str:
    """Convert bearing to 8-way compass label."""
    labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round(normalize_bearing(angle) / 45) % 8
    return labels[idx]


def direction_label(angle: float, bins: int = 8) -> str:
    """Return text label for angle. Currently supports 8 bins cleanly."""
    if bins != 8:
        raise NotImplementedError("Only 8-way labels implemented currently.")
    return bearing_to_compass(angle)


def bearing_difference(b1: float, b2: float) -> float:
    """Smallest angular difference between two bearings."""
    diff = abs(normalize_bearing(b1) - normalize_bearing(b2))
    return min(diff, 360 - diff)


def destination_point(p, bearing_deg, distance_km):
    """Compute destination from point, bearing, and distance."""
    raise NotImplementedError
```

## `src/wdo/geometry/interpolation.py`

```python
def interpolate_path(p1, p2, steps=10):
    """Return linear interpolation between two points."""
    lat1, lon1 = p1
    lat2, lon2 = p2
    return [
        (
            lat1 + (lat2 - lat1) * i / steps,
            lon1 + (lon2 - lon1) * i / steps,
        )
        for i in range(steps + 1)
    ]
```

## `src/wdo/geometry/simplify.py`

```python
def simplify_geometry(geometry, tolerance):
    """Simplify a geometry using shapely/geopandas-backed logic."""
    raise NotImplementedError


def simplify_geojson(data, tolerance):
    """Simplify every feature geometry in a GeoJSON-like structure."""
    raise NotImplementedError


def multi_level_simplify(data, tolerances):
    """Return dict of {name: simplified_data} for multiple tolerance levels."""
    raise NotImplementedError
```

---

## `src/wdo/spatial/__init__.py`

```python
from .feature_queries import *
from .intersections import *
from .buffers import *
from .pip import *
```

## `src/wdo/spatial/feature_queries.py`

```python
def filter_features(data, predicate):
    """Return FeatureCollection of features matching predicate(feature)."""
    raise NotImplementedError


def filter_by_property(data, key, value):
    """Return features where properties[key] == value."""
    raise NotImplementedError


def filter_by_property_range(data, key, low, high):
    """Return features where low <= properties[key] <= high."""
    raise NotImplementedError


def classify_point(point, features, label_key="name"):
    """Return label of first containing feature."""
    raise NotImplementedError
```

## `src/wdo/spatial/intersections.py`

```python
def path_to_segments(coords):
    """Convert ordered path coordinates into segment pairs."""
    return list(zip(coords[:-1], coords[1:]))


def segments_intersect(a1, a2, b1, b2) -> bool:
    """Return True if segments intersect."""
    raise NotImplementedError


def intersection_point(a1, a2, b1, b2):
    """Return intersection point if segments intersect."""
    raise NotImplementedError


def line_intersects_polygon(line, polygon) -> bool:
    """Return True if a line intersects a polygon."""
    raise NotImplementedError


def intersecting_features(line, features):
    """Return features intersecting the line."""
    raise NotImplementedError


def first_intersection(line, features):
    """Return first intersected feature, if any."""
    raise NotImplementedError
```

## `src/wdo/spatial/buffers.py`

```python
def buffer_point(point, distance, crs=None):
    """Return buffer geometry around a point."""
    raise NotImplementedError


def buffer_line(line, distance, crs=None):
    """Return buffer geometry around a line."""
    raise NotImplementedError


def multi_buffer(geometry, distances):
    """Return multiple buffer geometries for a list of distances."""
    raise NotImplementedError


def features_within_buffer(buffer_geom, features):
    """Return features intersecting or within a buffer."""
    raise NotImplementedError
```

## `src/wdo/spatial/pip.py`

```python
def ray_casting(point, polygon) -> bool:
    """Manual ray casting point-in-polygon check."""
    raise NotImplementedError


def point_in_polygon(point, polygon) -> bool:
    """Wrapper for current point-in-polygon implementation."""
    return ray_casting(point, polygon)


def containing_feature(point, features):
    """Return first containing feature."""
    raise NotImplementedError


def all_containing_features(point, features):
    """Return all containing features."""
    raise NotImplementedError
```

---

## `src/wdo/games/__init__.py`

```python
from .worldle import *
from .pursuit import *
```

## `src/wdo/games/worldle.py`

```python
def choose_target(features, seed=None):
    """Choose a target feature for Worldle++."""
    raise NotImplementedError


def feature_center(feature):
    """Return representative center point of a feature."""
    raise NotImplementedError


def guess_feedback(guess_feature, target_feature):
    """Return distance, bearing, and descriptive feedback."""
    raise NotImplementedError


def format_feedback(result) -> str:
    """Pretty-print guess feedback."""
    raise NotImplementedError
```

## `src/wdo/games/pursuit.py`

```python
def make_track(origin, bearing, speed_kmh):
    """Create a simple moving-object representation."""
    return {
        "origin": origin,
        "bearing": bearing,
        "speed_kmh": speed_kmh,
    }


def predict_position(origin, bearing, speed_kmh, minutes):
    """Predict future position under constant motion."""
    raise NotImplementedError


def time_to_intercept(*args, **kwargs):
    """Compute intercept time for simplified pursuit scenario."""
    raise NotImplementedError


def simulate_pursuit_step(target, pursuer, dt):
    """Advance target and pursuer one timestep."""
    raise NotImplementedError


def simulate_pursuit(target, pursuer, steps, dt):
    """Run a pursuit simulation for several steps."""
    raise NotImplementedError


def track_to_linestring(track_points):
    """Convert simulated points into a line/path representation."""
    return track_points


def can_intercept(target, pursuer, max_time=None):
    """Return whether intercept appears feasible under current model."""
    raise NotImplementedError
```

---

## `src/wdo/graphs/__init__.py`

```python
from .rail_graph import *
from .connectivity import *
from .routing import *
```

## `src/wdo/graphs/rail_graph.py`

```python
def extract_endpoints(feature):
    """Extract endpoints from a line-like feature."""
    raise NotImplementedError


def make_edge_weights(edges):
    """Attach weights (distances) to edges."""
    raise NotImplementedError


def build_graph_from_lines(features):
    """Convert railroad features into a graph structure."""
    raise NotImplementedError
```

## `src/wdo/graphs/connectivity.py`

```python
def connected_components(graph):
    """Return connected components of a graph."""
    raise NotImplementedError


def is_reachable(graph, start, goal) -> bool:
    """Return True if goal is reachable from start."""
    raise NotImplementedError
```

## `src/wdo/graphs/routing.py`

```python
def shortest_path(graph, start, goal):
    """Return shortest path between start and goal."""
    raise NotImplementedError


def path_length(graph, path):
    """Return total length of a path."""
    raise NotImplementedError
```

---

## `src/wdo/utils/__init__.py`

```python
from .formatting import *
from .validation import *
```

## `src/wdo/utils/formatting.py`

```python
def fmt_latlon(lat, lon, decimals=4) -> str:
    """Format coordinates for display."""
    return f"({lat:.{decimals}f}, {lon:.{decimals}f})"
```

## `src/wdo/utils/validation.py`

```python
def validate_basic_geojson(data) -> bool:
    """Basic check that object looks like GeoJSON."""
    return isinstance(data, dict) and "type" in data


def warn_if_geographic_crs(gdf) -> None:
    """Warn if operations are being done in geographic CRS."""
    raise NotImplementedError
```

---

# Suggested build order

Here’s the sane order. Not the heroic nonsense order.

## Phase 1: build these first

- `wdo.io.paths`
- `wdo.io.geojson_tools`
- `wdo.geometry.distance`
- `wdo.geometry.bearing`
- `wdo.geometry.bbox`

## Phase 2: then these

- `wdo.maps.leaflet_helpers`
- `wdo.maps.style_tools`
- `wdo.spatial.feature_queries`
- `wdo.spatial.pip`

## Phase 3: then these

- `wdo.spatial.intersections`
- `wdo.spatial.buffers`
- `wdo.geometry.simplify`

## Phase 4: project-specific

- `wdo.games.worldle`
- `wdo.graphs.rail_graph`
- `wdo.graphs.connectivity`
- `wdo.graphs.routing`

That order matches the course arc instead of making you implement graph routing before students can even load a feature collection without emotional damage.

---

# Best practical use

You could paste:

- the **table** into a planning README
- the **scaffold** into your repo
- then implement functions only when a notebook naturally earns them

That gives you structure without overcommitting.

Next move I’d recommend: I can turn this into a **bash or Python scaffold generator** that creates all these files automatically so you don’t have to hand-make them like it’s 1998.

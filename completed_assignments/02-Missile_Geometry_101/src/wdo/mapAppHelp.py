from __future__ import annotations

import json
from pathlib import Path

import ipywidgets as widgets
from IPython.display import display
from ipyleaflet import LayersControl, Map, Marker, WidgetControl


class GeoJsonHelp:
    """Small helper class for loading and inspecting GeoJSON data."""

    def __init__(self, path: Path | None = None):
        self.geojson_obj = None
        self.path = path
        if self.path is not None:
            self.load_geojson(self.path)

    def load_geojson(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(
                f"\n❌ ERROR: File not found:\n{path}\n"
                "Check spelling and folder structure."
            )

        self.geojson_obj = json.loads(path.read_text())
        return self.geojson_obj

    def get_features(self, geojson_obj):
        return geojson_obj.get("features", [])

    def extract_polygon_rings(self, feature):
        geom = feature["geometry"]
        coords = geom["coordinates"]

        if geom["type"] == "Polygon":
            return coords

        if geom["type"] == "MultiPolygon":
            rings = []
            for poly in coords:
                rings.extend(poly)
            return rings

        return []


class MapAppHelp:
    def __init__(self, points_file: Path, center=(40.0, -99.0), zoom=5):
        self.points_file = points_file
        self.clicked_points = self.load_points()
        self.markers = []

        self.map = Map(
            center=center,
            zoom=zoom,
            layout=widgets.Layout(width="100%", height="700px"),
        )
        self.map.add(LayersControl())

        self.output = widgets.Output()
        self.clear_btn = widgets.Button(description="Clear Saved Points")

        self.restore_markers()
        self.bind_events()
        self.add_controls()

    def load_points(self):
        if self.points_file.exists():
            text = self.points_file.read_text().strip()
            if text:
                return json.loads(text)
            return []

        self.points_file.parent.mkdir(parents=True, exist_ok=True)
        self.points_file.write_text("[]")
        return []

    def save_points(self):
        self.points_file.parent.mkdir(parents=True, exist_ok=True)
        self.points_file.write_text(json.dumps(self.clicked_points, indent=2))

    def restore_markers(self):
        for pt in self.clicked_points:
            marker = Marker(location=(pt["lat"], pt["lon"]))
            self.markers.append(marker)
            self.map.add(marker)

    def add_marker(self, lat: float, lon: float):
        marker = Marker(location=(lat, lon))
        self.markers.append(marker)
        self.map.add(marker)

    def log(self, message: str):
        with self.output:
            print(message)

    def handle_interaction(self, **kwargs):
        if kwargs.get("type") != "click":
            return

        lat, lon = kwargs["coordinates"]
        point = {"lat": round(lat, 6), "lon": round(lon, 6)}

        self.clicked_points.append(point)
        self.add_marker(point["lat"], point["lon"])
        self.save_points()
        self.log(f"Saved click: {point}")

    def clear_points(self, _):
        self.clicked_points.clear()
        self.save_points()

        for marker in list(self.markers):
            if marker in self.map.layers:
                self.map.remove(marker)

        self.markers.clear()
        self.log("Cleared saved points.")

    def bind_events(self):
        self.map.on_interaction(self.handle_interaction)
        self.clear_btn.on_click(self.clear_points)

    def add_controls(self):
        self.map.add(WidgetControl(widget=self.clear_btn, position="topright"))

    def display(self):
        display(self.map, self.output)

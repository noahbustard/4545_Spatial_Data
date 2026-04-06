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

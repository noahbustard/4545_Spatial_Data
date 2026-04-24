import asyncio

from wdo.geometry.bbox import bbox_from_feature, bbox_from_features, bbox_to_polygon


def _require_ipyleaflet():
    try:
        import ipyleaflet
    except ImportError as exc:
        raise ImportError(
            "ipyleaflet is required for wdo.maps.leaflet_helpers. "
            "Install the course requirements or run: pip install ipyleaflet ipywidgets"
        ) from exc
    return ipyleaflet


def _resolve_basemap(ipyleaflet, basemap):
    if basemap is None:
        return ipyleaflet.basemaps.OpenStreetMap.Mapnik

    if not isinstance(basemap, str):
        return basemap

    current = ipyleaflet.basemaps
    for part in basemap.split("."):
        current = getattr(current, part)
    return current


def _data_bbox(data):
    if isinstance(data, dict) and data.get("type") == "FeatureCollection":
        return bbox_from_features(data)
    if isinstance(data, dict) and data.get("type") == "Feature":
        return bbox_from_feature(data)
    if isinstance(data, dict) and "features" in data:
        return bbox_from_features(data.get("features", []))
    return bbox_from_feature(data)


def make_map(center=(0, 0), zoom=2, **kwargs):
    """Create and return an ipyleaflet Map with course-friendly defaults."""
    ipyleaflet = _require_ipyleaflet()
    basemap = _resolve_basemap(ipyleaflet, kwargs.pop("basemap", None))
    kwargs.setdefault("scroll_wheel_zoom", True)
    return ipyleaflet.Map(center=center, zoom=zoom, basemap=basemap, **kwargs)


def add_basemap(map_obj, name="OpenStreetMap"):
    """Add/select a basemap layer."""
    ipyleaflet = _require_ipyleaflet()
    basemap_name = "OpenStreetMap.Mapnik" if name == "OpenStreetMap" else name
    basemap = _resolve_basemap(ipyleaflet, basemap_name)
    layer = ipyleaflet.basemap_to_tiles(basemap)
    map_obj.add_layer(layer)
    return layer


def add_geojson(map_obj, data, name=None, style=None):
    """Add GeoJSON data to a map."""
    ipyleaflet = _require_ipyleaflet()
    default_style = {
        "color": "#1f6feb",
        "fillColor": "#2f81f7",
        "weight": 2,
        "fillOpacity": 0.35,
    }
    if style:
        default_style.update(style)

    layer = ipyleaflet.GeoJSON(data=data, name=name or "GeoJSON", style=default_style)
    map_obj.add_layer(layer)
    return layer


def fit_map_to_geojson(map_obj, data):
    """Adjust map viewport to fit GeoJSON bounds."""
    min_lon, min_lat, max_lon, max_lat = _data_bbox(data)
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        map_obj.center = ((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)
    else:
        map_obj.fit_bounds(bounds)
    return (min_lon, min_lat, max_lon, max_lat)


def add_layer_control(map_obj):
    """Add layer control widget."""
    ipyleaflet = _require_ipyleaflet()
    control = ipyleaflet.LayersControl(position="topright")
    map_obj.add_control(control)
    return control


def add_scale_control(map_obj):
    """Add scale control widget."""
    ipyleaflet = _require_ipyleaflet()
    control = ipyleaflet.ScaleControl(position="bottomleft")
    map_obj.add_control(control)
    return control


def add_bbox(map_obj, bbox, **style):
    """Draw a bounding box on the map."""
    ipyleaflet = _require_ipyleaflet()
    default_style = {
        "color": "#d73a49",
        "fillColor": "#d73a49",
        "weight": 2,
        "fillOpacity": 0.08,
    }
    default_style.update(style)
    layer = ipyleaflet.Polygon(locations=bbox_to_polygon(bbox), **default_style)
    map_obj.add_layer(layer)
    return layer


def add_path(map_obj, coords, **style):
    """Add a path/polyline to the map."""
    ipyleaflet = _require_ipyleaflet()
    default_style = {
        "color": "#f59e0b",
        "weight": 3,
        "opacity": 0.85,
    }
    default_style.update(style)
    layer = ipyleaflet.Polyline(locations=list(coords), **default_style)
    map_obj.add_layer(layer)
    return layer

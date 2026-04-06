def simplify_geometry(geometry, tolerance):
    """Simplify a geometry using shapely/geopandas-backed logic."""
    raise NotImplementedError


def simplify_geojson(data, tolerance):
    """Simplify every feature geometry in a GeoJSON-like structure."""
    raise NotImplementedError


def multi_level_simplify(data, tolerances):
    """Return dict of {name: simplified_data} for multiple tolerance levels."""
    raise NotImplementedError

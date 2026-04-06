def validate_basic_geojson(data) -> bool:
    """Basic check that object looks like GeoJSON."""
    return isinstance(data, dict) and "type" in data


def warn_if_geographic_crs(gdf) -> None:
    """Warn if operations are being done in geographic CRS."""
    raise NotImplementedError

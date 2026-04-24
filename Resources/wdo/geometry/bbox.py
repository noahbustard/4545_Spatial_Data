def _is_lon_lat_pair(value):
    return (
        isinstance(value, (list, tuple))
        and len(value) >= 2
        and isinstance(value[0], (int, float))
        and isinstance(value[1], (int, float))
    )


def _geometry_from_feature(feature):
    if not isinstance(feature, dict):
        raise TypeError("GeoJSON feature must be a dictionary.")

    if feature.get("type") == "Feature":
        geometry = feature.get("geometry")
    elif "geometry" in feature:
        geometry = feature.get("geometry")
    else:
        geometry = feature

    if not isinstance(geometry, dict):
        raise ValueError("GeoJSON feature has no geometry.")
    return geometry


def _iter_lon_lat_from_coordinates(coordinates):
    if _is_lon_lat_pair(coordinates):
        yield (float(coordinates[0]), float(coordinates[1]))
        return

    if isinstance(coordinates, (list, tuple)):
        for item in coordinates:
            yield from _iter_lon_lat_from_coordinates(item)


def _iter_lon_lat_from_geometry(geometry):
    geometry_type = geometry.get("type")

    if geometry_type == "GeometryCollection":
        for child in geometry.get("geometries", []):
            if isinstance(child, dict):
                yield from _iter_lon_lat_from_geometry(child)
        return

    yield from _iter_lon_lat_from_coordinates(geometry.get("coordinates", []))


def _iter_lon_lat_from_feature(feature):
    yield from _iter_lon_lat_from_geometry(_geometry_from_feature(feature))


def _features_from_input(features):
    if isinstance(features, dict) and features.get("type") == "FeatureCollection":
        return list(features.get("features", []))
    return list(features)


def bbox_from_points(points):
    """Return bbox as (min_lon, min_lat, max_lon, max_lat)."""
    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    return (min(lons), min(lats), max(lons), max(lats))


def bbox_from_feature(feature):
    """Return (min_lon, min_lat, max_lon, max_lat) for a GeoJSON feature.

    GeoJSON coordinates are stored as (lon, lat). This helper walks the nested
    coordinate arrays used by Polygon and MultiPolygon features, and also works
    for the simpler Point and LineString families.
    """
    points = list(_iter_lon_lat_from_feature(feature))
    if not points:
        raise ValueError("Cannot compute a bounding box for empty geometry.")

    lons = [point[0] for point in points]
    lats = [point[1] for point in points]
    return (min(lons), min(lats), max(lons), max(lats))


def bbox_from_features(features):
    """Return one bbox covering every feature in an iterable or FeatureCollection."""
    feature_list = _features_from_input(features)
    if not feature_list:
        raise ValueError("Cannot compute a bounding box for no features.")

    boxes = [bbox_from_feature(feature) for feature in feature_list]
    min_lons = [box[0] for box in boxes]
    min_lats = [box[1] for box in boxes]
    max_lons = [box[2] for box in boxes]
    max_lats = [box[3] for box in boxes]
    return (min(min_lons), min(min_lats), max(max_lons), max(max_lats))


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

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

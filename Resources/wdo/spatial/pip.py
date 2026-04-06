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

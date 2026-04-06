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

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

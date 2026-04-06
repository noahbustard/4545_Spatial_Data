import math


def valid_lat(lat: float) -> bool:
    return -90.0 <= lat <= 90.0


def valid_lon(lon: float) -> bool:
    return -180.0 <= lon <= 180.0


def valid_latlon(lat: float, lon: float) -> bool:
    return valid_lat(lat) and valid_lon(lon)


def make_point(lat: float, lon: float) -> tuple[float, float]:
    """Return a simple point as (lat, lon)."""
    return (lat, lon)


def point_to_lonlat(point: tuple[float, float]) -> tuple[float, float]:
    """Convert (lat, lon) to (lon, lat)."""
    lat, lon = point
    return (lon, lat)


def lat_degree_length() -> float:
    """Approximate meters per degree latitude."""
    return 111_320.0


def lon_degree_length_at_lat(lat: float) -> float:
    """Approximate meters per degree longitude at a given latitude."""
    return 111_320.0 * math.cos(math.radians(lat))

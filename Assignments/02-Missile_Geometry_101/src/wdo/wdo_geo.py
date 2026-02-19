"""
wdo_geo.py — World Defense Organization geometry helpers

This file is intentionally SMALL and focused:
- distance (haversine)
- bearing
- destination point
- interpolation for visualization (simple)
- bounding box helpers

It is NOT a GIS replacement.
It is a learning toolkit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import radians, degrees, sin, cos, asin, atan2, sqrt
from typing import Iterable, List, Sequence, Tuple


EARTH_RADIUS_KM: float = 6371.0088  # mean Earth radius (km) — good enough for class


@dataclass(frozen=True)
class LatLon:
    lat: float
    lon: float

    def as_tuple(self) -> Tuple[float, float]:
        return (self.lat, self.lon)


def _deg_to_rad(x: float) -> float:
    return radians(x)


def _rad_to_deg(x: float) -> float:
    return degrees(x)


def normalize_bearing_deg(bearing: float) -> float:
    """
    Normalize any angle into [0, 360).
    """
    b = bearing % 360.0
    return b if b >= 0 else b + 360.0


# ----------------------------------------
# Distance: Haversine (km)
# ----------------------------------------
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute great-circle distance between two lat/lon points.
    Returns distance in kilometers.
    Inputs: degrees
    Output: kilometers
    """
    phi1 = radians(lat1)
    phi2 = radians(lat2)

    dphi = radians(lat2 - lat1)
    dlmb = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlmb / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def initial_bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Initial bearing (forward azimuth) from point 1 to point 2.

    Inputs: degrees
    Output: degrees in [0, 360)
    """
    phi1 = _deg_to_rad(lat1)
    phi2 = _deg_to_rad(lat2)
    dlambda = _deg_to_rad(lon2 - lon1)

    y = sin(dlambda) * cos(phi2)
    x = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(dlambda)

    theta = atan2(y, x)  # radians
    return normalize_bearing_deg(_rad_to_deg(theta))


# ----------------------------------------
# Destination point (bearing + distance)
# ----------------------------------------
def destination_point(
    lat: float, lon: float, bearing_deg: float, distance_km: float
) -> LatLon:
    """
    Compute destination point given start, bearing, and distance on a sphere.

    Inputs:
      - lat, lon in degrees
      - bearing_deg in degrees
      - distance_km in kilometers
    Output:
      - LatLon (degrees)
    """
    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")

    phi1 = _deg_to_rad(lat)
    lambda1 = _deg_to_rad(lon)
    theta = _deg_to_rad(normalize_bearing_deg(bearing_deg))

    delta = distance_km / EARTH_RADIUS_KM  # angular distance in radians

    sin_phi2 = sin(phi1) * cos(delta) + cos(phi1) * sin(delta) * cos(theta)
    phi2 = asin(max(-1.0, min(1.0, sin_phi2)))

    y = sin(theta) * sin(delta) * cos(phi1)
    x = cos(delta) - sin(phi1) * sin(phi2)
    lambda2 = lambda1 + atan2(y, x)

    lat2 = _rad_to_deg(phi2)
    lon2 = _rad_to_deg(lambda2)

    # Normalize lon to [-180, 180)
    lon2 = ((lon2 + 180.0) % 360.0) - 180.0

    return LatLon(lat2, lon2)


# ----------------------------------------
# Interpolate Points (list of points)
# ----------------------------------------
def interpolate_latlon_linear(start: LatLon, end: LatLon, n: int) -> List[LatLon]:
    """
    Simple linear interpolation in lat/lon space.
    This is NOT geodesic interpolation. It's mainly for quick visualization.
    It generates points between a start and end.

    n = number of points INCLUDING endpoints (n >= 2)
    """
    if n < 2:
        raise ValueError("n must be >= 2")

    pts: List[LatLon] = []
    for i in range(n):
        t = i / (n - 1)
        lat = start.lat + t * (end.lat - start.lat)
        lon = start.lon + t * (end.lon - start.lon)
        pts.append(LatLon(lat, lon))
    return pts


# ----------------------------------------
# Trajectory sampling (list of points)
# ----------------------------------------
def trajectory_points(
    origin_lat: float,
    origin_lon: float,
    bearing_deg: float,
    speed_kmh: float,
    duration_min: float,
    step_min: float = 2.0,
) -> List[Tuple[float, float]]:
    """
    Generate intermediate (lat, lon) points along a trajectory.
    This function uses an origin and a bearing to generate points (no set destination).
    """
    points = [(origin_lat, origin_lon)]

    steps = max(1, int(duration_min / step_min))
    for i in range(1, steps + 1):
        elapsed_hr = (i * step_min) / 60.0
        dist_km = speed_kmh * elapsed_hr
        dest = destination_point(origin_lat, origin_lon, bearing_deg, dist_km)
        points.append((dest.lat, dest.lon))

    return points


# ----------------------------------------
# Bounding Box
# ----------------------------------------
def bbox_latlon(points: Sequence[LatLon]) -> Tuple[float, float, float, float]:
    """
    Bounding box for a list of LatLon: (min_lat, min_lon, max_lat, max_lon)
    """
    if not points:
        raise ValueError("points must be non-empty")

    lats = [p.lat for p in points]
    lons = [p.lon for p in points]
    return (min(lats), min(lons), max(lats), max(lons))

import math


def euclidean(p1, p2) -> float:
    """Naive planar distance between (lat, lon) points."""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def haversine_km(p1, p2) -> float:
    """Great-circle distance in kilometers between (lat, lon) points."""
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c


def haversine_miles(p1, p2) -> float:
    """Great-circle distance in miles."""
    return haversine_km(p1, p2) * 0.621371


def compare_distance_methods(p1, p2):
    """Return both Euclidean and haversine results for comparison."""
    return {
        "euclidean_deg": euclidean(p1, p2),
        "haversine_km": haversine_km(p1, p2),
        "haversine_miles": haversine_miles(p1, p2),
    }


def distances_from_point(point, points):
    """Return distances from one point to many points."""
    return [haversine_km(point, p) for p in points]


def pairwise_distances(points):
    """Return pairwise distance matrix as nested lists."""
    return [[haversine_km(a, b) for b in points] for a in points]


def distance_to_feature(point, feature):
    """Distance from point to a representative point of a feature."""
    raise NotImplementedError


def nearest_feature(point, features):
    """Return nearest feature and distance."""
    raise NotImplementedError

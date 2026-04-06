from .json_tools import load_json


def load_geojson(path):
    """Load GeoJSON from disk."""
    return load_json(path)


def is_feature(obj) -> bool:
    """Return True if object looks like a GeoJSON Feature."""
    return isinstance(obj, dict) and obj.get("type") == "Feature"


def is_feature_collection(obj) -> bool:
    """Return True if object looks like a GeoJSON FeatureCollection."""
    return isinstance(obj, dict) and obj.get("type") == "FeatureCollection"


def get_features(data):
    """Return features from a FeatureCollection, or [] if absent."""
    return data.get("features", []) if isinstance(data, dict) else []


def iter_features(data):
    """Yield each feature from GeoJSON data."""
    yield from get_features(data)


def feature_count(data) -> int:
    """Return number of features."""
    return len(get_features(data))


def get_geometry(feature):
    """Return geometry dict from a feature."""
    return feature.get("geometry", {})


def get_properties(feature):
    """Return properties dict from a feature."""
    return feature.get("properties", {})


def property_names(data) -> list[str]:
    """Return sorted union of property keys across all features."""
    keys = set()
    for feature in get_features(data):
        keys.update(get_properties(feature).keys())
    return sorted(keys)


def get_property(feature, key, default=None):
    """Safely retrieve a single property from a feature."""
    return get_properties(feature).get(key, default)

def filter_features(data, predicate):
    """Return FeatureCollection of features matching predicate(feature)."""
    raise NotImplementedError


def filter_by_property(data, key, value):
    """Return features where properties[key] == value."""
    raise NotImplementedError


def filter_by_property_range(data, key, low, high):
    """Return features where low <= properties[key] <= high."""
    raise NotImplementedError


def classify_point(point, features, label_key="name"):
    """Return label of first containing feature."""
    raise NotImplementedError

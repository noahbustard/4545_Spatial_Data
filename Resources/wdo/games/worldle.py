def choose_target(features, seed=None):
    """Choose a target feature for Worldle++."""
    raise NotImplementedError


def feature_center(feature):
    """Return representative center point of a feature."""
    raise NotImplementedError


def guess_feedback(guess_feature, target_feature):
    """Return distance, bearing, and descriptive feedback."""
    raise NotImplementedError


def format_feedback(result) -> str:
    """Pretty-print guess feedback."""
    raise NotImplementedError

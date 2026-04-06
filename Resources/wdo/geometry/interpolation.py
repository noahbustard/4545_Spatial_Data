def interpolate_path(p1, p2, steps=10):
    """Return linear interpolation between two points."""
    lat1, lon1 = p1
    lat2, lon2 = p2
    return [
        (
            lat1 + (lat2 - lat1) * i / steps,
            lon1 + (lon2 - lon1) * i / steps,
        )
        for i in range(steps + 1)
    ]

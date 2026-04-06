def buffer_point(point, distance, crs=None):
    """Return buffer geometry around a point."""
    raise NotImplementedError


def buffer_line(line, distance, crs=None):
    """Return buffer geometry around a line."""
    raise NotImplementedError


def multi_buffer(geometry, distances):
    """Return multiple buffer geometries for a list of distances."""
    raise NotImplementedError


def features_within_buffer(buffer_geom, features):
    """Return features intersecting or within a buffer."""
    raise NotImplementedError

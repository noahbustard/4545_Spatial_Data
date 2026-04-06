def bind_click_logger(map_obj):
    """Bind a click event that logs coordinates."""
    raise NotImplementedError


def capture_clicks(map_obj):
    """Capture click events from a map."""
    raise NotImplementedError


def extract_click_latlon(event):
    """Extract (lat, lon) from a click event structure."""
    raise NotImplementedError


def format_click(event) -> str:
    """Return a human-readable click description."""
    raise NotImplementedError


def replace_layer(map_obj, old_layer, new_layer):
    """Remove old layer and add new layer."""
    raise NotImplementedError


def popup_text(text: str):
    """Build popup content."""
    return str(text)


def add_marker_with_popup(map_obj, lat, lon, text):
    """Add marker and popup to map."""
    raise NotImplementedError

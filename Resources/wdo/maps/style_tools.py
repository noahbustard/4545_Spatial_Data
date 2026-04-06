def style_constant(color="blue", weight=2, fill_opacity=0.4):
    """Return a constant style dictionary/callable."""
    return {
        "color": color,
        "weight": weight,
        "fillOpacity": fill_opacity,
    }


def style_by_property(key, palette=None):
    """Return a style function keyed on a feature property."""
    raise NotImplementedError


def highlight_features(data, selected_ids, color="red"):
    """Return a modified/styled data structure highlighting selected features."""
    raise NotImplementedError


def buffer_style(distance):
    """Return style for a given buffer ring."""
    raise NotImplementedError

def fmt_latlon(lat, lon, decimals=4) -> str:
    """Format coordinates for display."""
    return f"({lat:.{decimals}f}, {lon:.{decimals}f})"

import random
from pathlib import Path

from wdo.geometry.bbox import bbox_from_feature, _iter_lon_lat_from_feature
from wdo.geometry.bearing import bearing_to_compass, initial_bearing
from wdo.geometry.distance import haversine_km, haversine_miles


ARROWS = {
    "N": "↑",
    "NE": "↗",
    "E": "→",
    "SE": "↘",
    "S": "↓",
    "SW": "↙",
    "W": "←",
    "NW": "↖",
}


COUNTRY_NAME_ALIASES = {
    "Czechia": "Czech Republic",
    "Eswatini": "Swaziland",
    "North Macedonia": "Macedonia",
    "United States of America": "United States of America",
}


ISO2_CODE_ALIASES = {
    "CN-TW": "tw",
}


def _feature_list(features):
    if isinstance(features, dict) and features.get("type") == "FeatureCollection":
        return list(features.get("features", []))
    return list(features)


def _properties(feature):
    return feature.get("properties", {}) if isinstance(feature, dict) else {}


def _clean_code(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_name(name):
    text = str(name or "").strip().lower()
    return "".join(ch for ch in text if ch.isalnum())


def country_name(feature):
    """Return the best display name available on a country feature."""
    props = _properties(feature)
    return (
        props.get("ADMIN")
        or props.get("name")
        or props.get("NAME")
        or props.get("SOVEREIGNT")
        or "Unknown country"
    )


def country_iso3(feature):
    """Return a feature's ISO-3 code when available."""
    props = _properties(feature)
    return _clean_code(
        props.get("ISO_A3")
        or props.get("ISO3166-1-Alpha-3")
        or props.get("iso3")
        or props.get("ISO3")
    )


def country_iso2(feature):
    """Return a feature's ISO-2 code when available."""
    props = _properties(feature)
    return _clean_code(
        props.get("ISO_A2")
        or props.get("ISO3166-1-Alpha-2")
        or props.get("iso2")
        or props.get("ISO2")
    )


def build_country_lookup(
    countries_geojson,
    flag_index,
    aliases=None,
    flag_base_dir=None,
    flag_ratio="4x3",
):
    """Return {iso3: metadata} by joining country features to flag metadata.

    The current course data already includes ISO-2 codes on the country
    features. Name aliases remain here because other versions of the assignment
    data only provide names and ISO-3 codes.
    """
    aliases = {**COUNTRY_NAME_ALIASES, **(aliases or {})}
    features = _feature_list(countries_geojson)

    flag_rows = list(flag_index.values()) if isinstance(flag_index, dict) else list(flag_index)
    flags_by_code = {}
    flags_by_name = {}
    for row in flag_rows:
        code = _clean_code(row.get("code") if isinstance(row, dict) else None)
        name = row.get("name") if isinstance(row, dict) else None
        if code:
            flags_by_code[code.lower()] = row
        if name:
            flags_by_name[_normalize_name(name)] = row

    field_name = "flag_1x1" if str(flag_ratio) == "1x1" else "flag_4x3"
    lookup = {}
    for feature in features:
        name = country_name(feature)
        iso3 = country_iso3(feature)
        lookup_key = iso3 if iso3 and iso3 != "-99" else name
        iso2 = country_iso2(feature)

        flag_row = None
        if iso2:
            flag_code = ISO2_CODE_ALIASES.get(iso2.upper(), iso2.lower())
            flag_row = flags_by_code.get(flag_code)

        if flag_row is None:
            aliased_name = aliases.get(name, name)
            flag_row = flags_by_name.get(_normalize_name(aliased_name))

        flag_path = flag_row.get(field_name) if flag_row else None
        if flag_path and flag_base_dir is not None:
            flag_path = str(Path(flag_base_dir) / flag_path)

        lookup[lookup_key] = {
            "name": name,
            "iso2": iso2,
            "iso3": iso3,
            "flag_path": flag_path,
            "flag_found": flag_path is not None,
        }

    return lookup


def choose_target(features, seed=None):
    """Choose one GeoJSON feature at random, reproducibly when seed is given."""
    choices = _feature_list(features)
    if not choices:
        raise ValueError("choose_target needs at least one feature.")
    return random.Random(seed).choice(choices)


def feature_center(feature, method="bbox"):
    """Return a representative (lat, lon) point for a GeoJSON feature.

    method="bbox" returns the bounding-box center. method="mean" averages all
    boundary vertices. Both are intentionally simple for this course project.
    """
    if method == "bbox":
        min_lon, min_lat, max_lon, max_lat = bbox_from_feature(feature)
        return ((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)

    if method == "mean":
        points = list(_iter_lon_lat_from_feature(feature))
        if not points:
            raise ValueError("Cannot compute a center for empty geometry.")
        lon = sum(point[0] for point in points) / len(points)
        lat = sum(point[1] for point in points) / len(points)
        return (lat, lon)

    raise ValueError('method must be "bbox" or "mean".')


def guess_feedback(guess_feature, target_feature):
    """Compare a guess to the target and return Worldle feedback fields."""
    guess_center = feature_center(guess_feature)
    target_center = feature_center(target_feature)
    distance_km = haversine_km(guess_center, target_center)
    distance_miles = haversine_miles(guess_center, target_center)
    bearing_deg = initial_bearing(guess_center, target_center)
    compass = bearing_to_compass(bearing_deg)

    guess_iso = country_iso3(guess_feature)
    target_iso = country_iso3(target_feature)
    same_iso = bool(guess_iso and target_iso and guess_iso == target_iso and guess_iso != "-99")
    same_name = _normalize_name(country_name(guess_feature)) == _normalize_name(
        country_name(target_feature)
    )
    correct = same_iso or same_name

    return {
        "correct": correct,
        "guess_name": country_name(guess_feature),
        "target_name": country_name(target_feature),
        "guess_iso3": guess_iso,
        "target_iso3": target_iso,
        "guess_center": guess_center,
        "target_center": target_center,
        "distance_km": distance_km,
        "distance_miles": distance_miles,
        "bearing_deg": bearing_deg,
        "compass": compass,
        "arrow": ARROWS.get(compass, "?"),
    }


def format_feedback(result, units="km") -> str:
    """Return a plain-text feedback line for testing or logging."""
    if result.get("correct"):
        return f"Correct: {result.get('target_name', 'the target')}!"

    if units == "miles":
        distance = result["distance_miles"]
        unit_label = "mi"
    else:
        distance = result["distance_km"]
        unit_label = "km"

    return (
        f"{result.get('guess_name', 'Guess')}: "
        f"{result.get('arrow', '?')} {distance:,.0f} {unit_label} "
        f"{result.get('compass', '')} toward the target"
    )

#!/usr/bin/env python3
"""
summarize.py — Scan directories for data files and write a Markdown inventory report.

For each supported file found, the report includes:
  - Full path and file size
  - Format-specific summary (row/column counts, GeoJSON feature info, etc.)
  - A small data preview (first few rows of CSV, first record of JSON)

Output is a single Markdown file, organized by directory, with a summary table
at the top. Useful for documenting what data you have before sharing with students
or publishing a dataset collection.

Usage:
    # Scan one directory
    python summarize.py raw/csv/

    # Scan multiple directories
    python summarize.py raw/ processed/

    # Scan specific paths and write to a named output file
    python summarize.py raw/geojson/ processed/csv/ --output my_inventory.md

    # Control how many preview rows appear per file (default: 3)
    python summarize.py raw/ --preview-rows 5

    # Skip the data preview section entirely
    python summarize.py raw/ --no-preview

Supported formats: .csv  .tsv  .json  .geojson  .xml
"""

import argparse
import csv
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path


SUPPORTED_EXTENSIONS = {".csv", ".tsv", ".json", ".geojson", ".xml"}


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def human_size(n_bytes: int) -> str:
    """Convert bytes to a human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} TB"


def md_escape(text: str) -> str:
    """Escape pipe characters so strings don't break Markdown tables."""
    return str(text).replace("|", "\\|").replace("\n", " ")


# ---------------------------------------------------------------------------
# Per-format analyzers
# ---------------------------------------------------------------------------


def analyze_csv(path: Path, preview_rows: int) -> dict:
    """
    Returns summary dict and a list of preview row dicts for CSV/TSV.
    Handles Excel BOM (utf-8-sig) and auto-detects delimiter.
    """
    result = {"format": "CSV/TSV"}
    preview = []

    try:
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
            sample = f.read(8192)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",\t|;")
            except csv.Error:
                dialect = csv.excel
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)
            rows = list(reader)

        headers = list(rows[0].keys()) if rows else []
        result.update(
            {
                "row_count": len(rows),
                "column_count": len(headers),
                "columns": headers,
                "delimiter": repr(dialect.delimiter),
                "has_header": True,
            }
        )

        # Detect likely numeric columns (>80% of values parse as float)
        numeric_cols = []
        for col in headers:
            vals = [r.get(col, "") for r in rows if r.get(col, "").strip()]
            if not vals:
                continue
            try:
                parsed = sum(1 for v in vals if _is_numeric(v))
                if parsed / len(vals) > 0.8:
                    numeric_cols.append(col)
            except Exception:
                pass
        if numeric_cols:
            result["likely_numeric_columns"] = numeric_cols

        preview = rows[:preview_rows]

    except Exception as e:
        result["error"] = str(e)

    return result, preview


def _is_numeric(value: str) -> bool:
    try:
        float(value.replace(",", ""))
        return True
    except ValueError:
        return False


def analyze_json(path: Path, preview_rows: int) -> dict:
    """Returns summary dict and preview for JSON / GeoJSON."""
    result = {"format": "JSON"}
    preview = []

    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            data = json.load(f)

        # GeoJSON FeatureCollection
        if isinstance(data, dict) and data.get("type") == "FeatureCollection":
            features = data.get("features", [])
            geom_types = list(
                {
                    f.get("geometry", {}).get("type")
                    for f in features
                    if isinstance(f.get("geometry"), dict)
                }
            )
            prop_keys = []
            if features and isinstance(features[0].get("properties"), dict):
                prop_keys = list(features[0]["properties"].keys())

            result.update(
                {
                    "format": "GeoJSON",
                    "geojson_type": "FeatureCollection",
                    "feature_count": len(features),
                    "geometry_types": geom_types,
                    "property_keys": prop_keys,
                    "property_count": len(prop_keys),
                }
            )
            # Preview: first N feature property dicts
            preview = [f.get("properties", {}) for f in features[:preview_rows]]

        # JSON array of objects
        elif isinstance(data, list):
            result.update(
                {
                    "format": "JSON (array)",
                    "record_count": len(data),
                }
            )
            if data and isinstance(data[0], dict):
                result["first_item_keys"] = list(data[0].keys())
            preview = data[:preview_rows] if isinstance(data[0], dict) else []

        # JSON object
        elif isinstance(data, dict):
            result.update(
                {
                    "format": "JSON (object)",
                    "top_level_keys": list(data.keys()),
                    "key_count": len(data),
                }
            )

    except json.JSONDecodeError as e:
        result["error"] = f"JSON parse error: {e}"
    except Exception as e:
        result["error"] = str(e)

    return result, preview


def analyze_xml(path: Path, preview_rows: int) -> dict:
    """Returns a lightweight summary for XML files."""
    result = {"format": "XML"}
    preview = []

    try:
        tree = ET.parse(path)
        root = tree.getroot()
        tag = (
            root.tag.split("}")[-1] if "}" in root.tag else root.tag
        )  # strip namespace

        # Count direct children by tag
        child_tags: dict[str, int] = {}
        for child in root:
            t = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            child_tags[t] = child_tags.get(t, 0) + 1

        result.update(
            {
                "root_element": tag,
                "child_element_types": child_tags,
                "total_direct_children": sum(child_tags.values()),
                "root_attributes": dict(root.attrib) if root.attrib else None,
            }
        )

    except ET.ParseError as e:
        result["error"] = f"XML parse error: {e}"
    except Exception as e:
        result["error"] = str(e)

    return result, preview


def analyze_file(path: Path, preview_rows: int) -> tuple[dict, list]:
    """Dispatch to the right analyzer based on file extension."""
    ext = path.suffix.lower()
    if ext in {".csv", ".tsv"}:
        return analyze_csv(path, preview_rows)
    elif ext in {".json", ".geojson"}:
        return analyze_json(path, preview_rows)
    elif ext == ".xml":
        return analyze_xml(path, preview_rows)
    return {"format": "Unknown"}, []


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def render_summary_table(all_files: list[dict]) -> str:
    """Top-level summary table: one row per file."""
    lines = [
        "| File | Format | Size | Key Stats |",
        "|------|--------|------|-----------|",
    ]
    for entry in all_files:
        info = entry["info"]
        fname = md_escape(entry["path"].name)
        fmt = md_escape(info.get("format", "—"))
        size = md_escape(human_size(entry["size_bytes"]))

        # Build a short stat string
        stat_parts = []
        if "row_count" in info:
            stat_parts.append(
                f"{info['row_count']:,} rows × {info['column_count']} cols"
            )
        if "feature_count" in info:
            geom = ", ".join(info.get("geometry_types", [])) or "unknown geometry"
            stat_parts.append(f"{info['feature_count']:,} features ({geom})")
        if "record_count" in info:
            stat_parts.append(f"{info['record_count']:,} records")
        if "total_direct_children" in info:
            stat_parts.append(f"{info['total_direct_children']:,} child elements")
        if "error" in info:
            stat_parts.append(f"⚠ {info['error']}")

        stats = md_escape("; ".join(stat_parts) if stat_parts else "—")
        lines.append(f"| `{fname}` | {fmt} | {size} | {stats} |")

    return "\n".join(lines)


def render_csv_preview(headers: list[str], rows: list[dict]) -> str:
    """Render a small Markdown table from CSV preview rows."""
    if not rows or not headers:
        return "_No preview available._"

    # Truncate wide values for readability
    def trunc(v: str, n: int = 30) -> str:
        s = str(v)
        return s if len(s) <= n else s[: n - 1] + "…"

    header_row = "| " + " | ".join(md_escape(h) for h in headers) + " |"
    sep_row = "| " + " | ".join("---" for _ in headers) + " |"
    data_rows = [
        "| " + " | ".join(md_escape(trunc(row.get(h, ""))) for h in headers) + " |"
        for row in rows
    ]
    return "\n".join([header_row, sep_row] + data_rows)


def render_json_preview(rows: list[dict]) -> str:
    """Render JSON preview records as a fenced JSON block."""
    if not rows:
        return "_No preview available._"
    try:
        snippet = json.dumps(rows, indent=2, ensure_ascii=False)
        return f"```json\n{snippet}\n```"
    except Exception:
        return "_Preview unavailable._"


def render_file_section(entry: dict, show_preview: bool) -> str:
    """Render the full Markdown section for one file."""
    path = entry["path"]
    info = entry["info"]
    preview_data = entry["preview"]
    size = human_size(entry["size_bytes"])
    mtime = entry["mtime"].strftime("%Y-%m-%d %H:%M UTC")

    lines = [f"### `{path.name}`\n"]
    lines.append(f"**Path:** `{entry['rel_path']}`  ")
    lines.append(f"**Size:** {size}  ")
    lines.append(f"**Modified:** {mtime}  ")
    lines.append(f"**Format:** {info.get('format', '—')}  \n")

    if "error" in info:
        lines.append(f"> ⚠️ **Parse error:** {info['error']}\n")
        return "\n".join(lines)

    fmt = info.get("format", "")

    # --- CSV/TSV ---
    if fmt == "CSV/TSV":
        lines.append(f"- **Rows:** {info.get('row_count', '—'):,}")
        lines.append(f"- **Columns:** {info.get('column_count', '—')}")
        lines.append(f"- **Delimiter:** {info.get('delimiter', '—')}")
        cols = info.get("columns", [])
        if cols:
            col_list = ", ".join(f"`{c}`" for c in cols)
            lines.append(f"- **Column names:** {col_list}")
        num_cols = info.get("likely_numeric_columns", [])
        if num_cols:
            lines.append(
                f"- **Likely numeric:** {', '.join(f'`{c}`' for c in num_cols)}"
            )
        lines.append("")
        if show_preview and preview_data:
            lines.append("**Preview:**\n")
            lines.append(render_csv_preview(info.get("columns", []), preview_data))

    # --- GeoJSON ---
    elif fmt == "GeoJSON":
        lines.append(f"- **Features:** {info.get('feature_count', '—'):,}")
        geom = ", ".join(info.get("geometry_types", [])) or "—"
        lines.append(f"- **Geometry types:** {geom}")
        prop_keys = info.get("property_keys", [])
        if prop_keys:
            lines.append(
                f"- **Properties ({len(prop_keys)}):** {', '.join(f'`{k}`' for k in prop_keys)}"
            )
        lines.append("")
        if show_preview and preview_data:
            lines.append("**First feature properties:**\n")
            lines.append(render_json_preview(preview_data))

    # --- JSON array ---
    elif fmt == "JSON (array)":
        lines.append(f"- **Records:** {info.get('record_count', '—'):,}")
        keys = info.get("first_item_keys", [])
        if keys:
            lines.append(
                f"- **First record keys:** {', '.join(f'`{k}`' for k in keys)}"
            )
        lines.append("")
        if show_preview and preview_data:
            lines.append("**Preview:**\n")
            lines.append(render_json_preview(preview_data))

    # --- JSON object ---
    elif fmt == "JSON (object)":
        keys = info.get("top_level_keys", [])
        lines.append(
            f"- **Top-level keys ({len(keys)}):** {', '.join(f'`{k}`' for k in keys)}"
        )
        lines.append("")

    # --- XML ---
    elif fmt == "XML":
        lines.append(f"- **Root element:** `{info.get('root_element', '—')}`")
        child_tags = info.get("child_element_types", {})
        if child_tags:
            tag_str = ", ".join(f"`{t}` ({n:,})" for t, n in child_tags.items())
            lines.append(f"- **Direct child elements:** {tag_str}")
        attrs = info.get("root_attributes")
        if attrs:
            attr_str = ", ".join(f"`{k}`=`{v}`" for k, v in attrs.items())
            lines.append(f"- **Root attributes:** {attr_str}")
        lines.append("")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main report builder
# ---------------------------------------------------------------------------


def collect_files(scan_paths: list[Path]) -> list[dict]:
    """Walk all scan paths and return a list of file entry dicts."""
    seen = set()
    entries = []

    for scan_root in scan_paths:
        if not scan_root.exists():
            print(f"  WARNING: Path not found, skipping: {scan_root}", file=sys.stderr)
            continue

        paths = [scan_root] if scan_root.is_file() else sorted(scan_root.rglob("*"))

        for path in paths:
            if not path.is_file():
                continue
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            entries.append(path)

    return entries


def build_report(
    scan_paths: list[Path],
    output: Path,
    preview_rows: int,
    show_preview: bool,
) -> None:
    print(f"Scanning {len(scan_paths)} path(s)...")
    file_paths = collect_files(scan_paths)

    if not file_paths:
        print("No supported data files found.")
        return

    # Use the common ancestor of all scan_paths as the display root
    try:
        display_root = Path(os.path.commonpath([str(p.resolve()) for p in scan_paths]))
    except ValueError:
        display_root = scan_paths[0].resolve()

    # Analyze all files
    all_entries = []
    for path in file_paths:
        print(f"  analyzing: {path}")
        stat = path.stat()
        info, preview = analyze_file(path, preview_rows)
        try:
            rel = path.resolve().relative_to(display_root.resolve())
        except ValueError:
            rel = path
        all_entries.append(
            {
                "path": path,
                "rel_path": str(rel),
                "size_bytes": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                "info": info,
                "preview": preview,
            }
        )

    # Group by parent directory (relative)
    by_dir: dict[str, list] = {}
    for entry in all_entries:
        parent = str(Path(entry["rel_path"]).parent)
        by_dir.setdefault(parent, []).append(entry)

    # Build Markdown
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    scanned_str = ", ".join(f"`{p}`" for p in scan_paths)
    total_size = human_size(sum(e["size_bytes"] for e in all_entries))

    md = StringIO()
    md.write(f"# Data File Inventory\n\n")
    md.write(f"**Generated:** {now}  \n")
    md.write(f"**Paths scanned:** {scanned_str}  \n")
    md.write(f"**Files found:** {len(all_entries)}  \n")
    md.write(f"**Total size:** {total_size}  \n\n")
    md.write("---\n\n")

    # Table of contents
    md.write("## Contents\n\n")
    md.write("- [Summary Table](#summary-table)\n")
    for dir_name in sorted(by_dir.keys()):
        anchor = (
            dir_name.lower()
            .replace("/", "")
            .replace("\\", "")
            .replace(" ", "-")
            .replace(".", "")
        )
        label = dir_name if dir_name != "." else "(root)"
        md.write(f"- [{label}](#{anchor})\n")
    md.write("\n---\n\n")

    # Summary table
    md.write("## Summary Table\n\n")
    md.write(render_summary_table(all_entries))
    md.write("\n\n---\n\n")

    # Per-directory sections
    md.write("## File Details\n\n")
    for dir_name in sorted(by_dir.keys()):
        label = dir_name if dir_name != "." else "(root)"
        md.write(f"### {label}\n\n")
        for entry in by_dir[dir_name]:
            # Subsection header is h4 inside the directory h3
            md.write(render_file_section(entry, show_preview).replace("### ", "#### "))
        md.write("---\n\n")

    # Write output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(md.getvalue(), encoding="utf-8")
    print(f"\nReport written → {output}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for data files and write a Markdown inventory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="One or more directories (or files) to scan",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output Markdown file (default: inventory_YYYYMMDD.md in cwd)",
    )
    parser.add_argument(
        "--preview-rows",
        type=int,
        default=3,
        metavar="N",
        help="Number of preview rows per file (default: 3)",
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Omit data previews (faster, smaller output)",
    )
    args = parser.parse_args()

    # Default output filename: inventory_YYYYMMDD.md in cwd
    if args.output is None:
        stamp = datetime.now().strftime("%Y%m%d")
        args.output = Path(f"inventory_{stamp}.md")

    build_report(
        scan_paths=args.paths,
        output=args.output,
        preview_rows=args.preview_rows,
        show_preview=not args.no_preview,
    )


if __name__ == "__main__":
    main()

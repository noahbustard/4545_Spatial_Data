from pathlib import Path


def cwd() -> Path:
    """Return the current working directory."""
    return Path.cwd()


def path_exists(path) -> bool:
    """Return True if path exists."""
    return Path(path).exists()


def is_file(path) -> bool:
    """Return True if path is a file."""
    return Path(path).is_file()


def is_dir(path) -> bool:
    """Return True if path is a directory."""
    return Path(path).is_dir()


def abs_path(path) -> Path:
    """Return absolute path without necessarily resolving symlinks."""
    return Path(path).absolute()


def resolve_path(path) -> Path:
    """Return fully resolved path."""
    return Path(path).resolve()


def join_path(*parts) -> Path:
    """Join path parts safely."""
    return Path(*parts)


def find_upwards(target_name: str, start_path=".") -> Path | None:
    """Walk upward from start_path until target_name is found."""
    current = Path(start_path).resolve()
    for parent in [current, *current.parents]:
        if (parent / target_name).exists():
            return parent / target_name
    return None


def find_project_root(marker: str = ".git", start_path=".") -> Path | None:
    """Find project root by locating marker directory/file."""
    found = find_upwards(marker, start_path)
    return found.parent if found else None


def project_data_path(*parts, marker: str = ".git", start_path=".") -> Path:
    """Return a path inside the project's data folder."""
    root = find_project_root(marker=marker, start_path=start_path)
    if root is None:
        raise FileNotFoundError(f"Could not find project root using marker={marker!r}")
    return root / "data" / Path(*parts)

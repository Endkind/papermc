import os
from pathlib import Path
from typing import List, Tuple

from .argparser import get_default_argparse
from .docker import DockerHelper
from .minecraft import MinecraftHelper
from .validation import validation_error_to_result


def _parse_version_key(tag: str) -> Tuple:
    """
    Parse a version tag into a tuple for sorting purposes.
    Handles semantic versioning with pre-release identifiers.

    Args:
        tag: Version tag string (e.g., "1.21.9-pre2", "1.21.9", "latest")

    Returns:
        Tuple: Sortable tuple where "latest" sorts last, and versions sort naturally
    """
    if tag == "latest":
        return (float("inf"),)

    try:
        version_part = tag.split("-")[0]
        version_numbers = [int(x) for x in version_part.split(".")]

        if "-" in tag:
            pre_release = tag.split("-", 1)[1]
            return tuple(version_numbers + [0, pre_release])
        else:
            return tuple(version_numbers + [1])

    except ValueError:
        return (tag,)


def discover_versions() -> List[str]:
    versions = []
    versions_dir = get_versions_dir()

    for item in os.listdir(versions_dir):
        item_path = os.path.join(versions_dir, item)

        if not os.path.isdir(item_path):
            continue

        disabled_file = os.path.join(item_path, ".disabled")

        if os.path.exists(disabled_file):
            continue

        versions.append(item)

    def sort_key(version: str) -> str:
        return _parse_version_key(version)

    return sorted(versions, key=sort_key)


def get_versions_dir() -> Path:
    current_dir = Path(__file__).resolve().parent
    versions_dir = current_dir.parent / "versions"
    return versions_dir

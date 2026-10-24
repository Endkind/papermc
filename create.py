import argparse
import logging
import shutil
from pathlib import Path
from test import test

from result import Err, Ok, Result, is_err

from build import build
from logger import setup_logging
from utils import get_default_argparse, get_versions_dir

LOGGING_LEVELS = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}

VERSION_TEMPLATE_PATH = get_versions_dir() / "template"
TEMPLATE_FILES_TO_RENDER = ["Dockerfile", "README.md"]


def main():
    args = get_args()

    setup_logging(args.verbosity, min_module_width=6)

    create_version_result = create_version(args.version, args.java_version)
    if is_err(create_version_result):
        logging.error(f"Failed to create version: {create_version_result.err()}")
        exit(1)

    build_version_result = build(args.version)
    if is_err(build_version_result):
        logging.error(f"Failed to build version: {build_version_result.err()}")

        remove_version(args.version).unwrap_or_else(
            lambda err: logging.error(
                f"Failed to remove version after build failure: {err}"
            )
        )

        exit(1)
    logging.info(build_version_result.unwrap())

    test_version_result = test(args.version)
    if is_err(test_version_result):
        logging.error(f"Failed to test version: {test_version_result.err()}")

        remove_version(args.version).unwrap_or_else(
            lambda err: logging.error(
                f"Failed to remove version after test failure: {err}"
            )
        )

        exit(1)
    logging.info(test_version_result.unwrap())


def create_version(version: str, java_version: str) -> Result[None, str]:
    logging.info(f"Creating version {version} with Java {java_version}")

    version_dir = get_versions_dir() / version

    logging.debug("Checking if version directory already exists")
    if version_dir.exists():
        return Err(f"Version {version} already exists.")

    try:
        logging.debug("Copying version template")
        shutil.copytree(VERSION_TEMPLATE_PATH, version_dir)

        for file_name in TEMPLATE_FILES_TO_RENDER:
            template_path = version_dir / file_name

            logging.debug(f"Rendering template file {template_path}")
            render_template_file(template_path, version, java_version)

    except OSError as error:
        remove_version(version)

        return Err(f"Failed to create version {version}: {error}")

    return Ok(None)


def remove_version(version: str) -> Result[None, str]:
    logging.info(f"Removing version {version}")

    version_dir = get_versions_dir() / version

    if not version_dir.exists():
        return Err(f"Version {version} does not exist.")

    try:
        shutil.rmtree(version_dir)
    except OSError as error:
        remove_version(version).unwrap_or_else(
            lambda err: logging.error(
                f"Failed to remove version after build failure: {err}"
            )
        )

        return Err(f"Failed to remove version {version}: {error}")

    return Ok(None)


def render_template_file(template_path: Path, version: str, java_version: str) -> None:
    content = template_path.read_text(encoding="utf-8")

    replacements = {"{{VERSION}}": version, "{{JAVA_VERSION}}": java_version}

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    template_path.write_text(content, encoding="utf-8")


# region args
def get_args() -> argparse.Namespace:
    parser = get_default_argparse("Create a new version of PaperMC Docker image.")

    parser.add_argument("version", type=str, help="The new version to create.")
    parser.add_argument(
        "--java-version",
        "-j",
        type=str,
        default="21",
        help="The Java version to use for the new version.",
    )

    return parser.parse_args()


# endregion args

if __name__ == "__main__":
    main()

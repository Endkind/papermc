import argparse
import logging
import os
import subprocess
from typing import List

from result import Err, Ok, Result, is_err, is_ok

from config.docker import DockerConfig
from logger import setup_logging
from utils import discover_versions, get_default_argparse


def main():
    args = get_args()

    setup_logging(args.verbosity)

    if args.version:
        result = build_all(args.version)
    else:
        result = build_all()

    if is_ok(result):
        logging.info(f"Build process succeeded: {result.unwrap()}")
    elif is_err(result):
        logging.error(f"Build process failed: {result.unwrap_err()}")
        exit(1)


# region args
def get_args() -> argparse.Namespace:
    parser = get_default_argparse("Build a version(s) of PaperMC Docker image.")

    parser.add_argument(
        "version",
        nargs="*",
        help="The version(s) to build. If omitted, all versions will be built.",
    )

    return parser.parse_args()


# endregion args


# region build
def build(tag: str) -> Result[str, str]:
    """
    Build a Docker image with the specified tag.

    Args:
        tag: The tag of the image

    Returns:
        Result[str, str]: Ok with success message or Err with error message
    """
    try:
        image_name = f"endkind/{DockerConfig.IMAGE_NAME}:{tag}"

        context_path = f"./versions/{tag}"

        if not os.path.exists(context_path):
            return Err(f"Build context path '{context_path}' does not exist")

        cmd = ["docker", "build", "-t", image_name, context_path]

        logging.debug(f"Building Docker image: {image_name}")
        logging.debug(f"Build context: {context_path}")
        logging.debug(f"Command: {' '.join(cmd)}")

        subprocess.run(cmd, capture_output=True, text=True, check=True)

        if len(DockerConfig.ALT_IMAGE_NAME) > 0:
            for alt_name in DockerConfig.ALT_IMAGE_NAME:
                alt_image_name = f"endkind/{alt_name}:{tag}"
                tag_cmd = ["docker", "tag", image_name, alt_image_name]
                logging.debug(f"Tagging Docker image: {alt_image_name}")
                logging.debug(f"Command: {' '.join(tag_cmd)}")
                subprocess.run(tag_cmd, capture_output=True, text=True, check=True)

        return Ok(f"Docker image '{image_name}' built successfully")

    except subprocess.CalledProcessError as e:
        error_msg = f"Docker build failed: {e.stderr if e.stderr else e.stdout}"
        return Err(error_msg)
    except Exception as e:
        return Err(f"Unexpected error: {str(e)}")


def build_all(versions: List[str] = discover_versions()) -> Result[str, str]:
    """
    Build all available Docker images by auto-discovering available configurations.
    """

    if not versions:
        return Err("No build configurations found!")

    logging.debug(f"Found {len(versions)} build configurations:")
    for version in versions:
        logging.debug(f" - {DockerConfig.IMAGE_NAME}:{version}")
    logging.debug("")

    logging.info("Starting builds...")
    logging.info("")

    success_count = 0

    for version in versions:
        logging.info(f"--- Building {DockerConfig.IMAGE_NAME}:{version} ---")
        result = build(version)

        if is_ok(result):
            logging.info(f"✅ {result.unwrap()}")
            success_count += 1
        else:
            logging.error(f"❌ {result.unwrap_err()}")

    if success_count < len(versions):
        return Err(f"Build incomplete: only {success_count}/{len(versions)} succeeded")
    return Ok(f"Build complete: {success_count}/{len(versions)} succeeded")


# endregion build

if __name__ == "__main__":
    main()

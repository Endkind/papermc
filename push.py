import subprocess
from typing import List

from result import Err, Ok, Result, is_err, is_ok

from utils import discover_versions


def main():
    result = push_all()
    if is_err(result):
        print(f"Push process failed: {result.unwrap_err()}")


def push(tag: str) -> Result[str, str]:
    """
    Push a Docker image with the specified tag to Docker Hub.

    Args:
        tag: The tag of the image

    Returns:
        Result[str, str]: Ok with success message or Err with error message
    """
    try:
        image_name = f"endkind/papermc:{tag}"

        cmd = ["docker", "push", image_name]

        print(f"Pushing Docker image: {image_name}")
        print(f"Command: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        return Ok(f"Docker image '{image_name}' pushed successfully")

    except subprocess.CalledProcessError as e:
        error_msg = f"Docker push failed: {e.stderr if e.stderr else e.stdout}"
        return Err(error_msg)
    except Exception as e:
        return Err(f"Unexpected error: {str(e)}")


def push_all(versions: List[str] = discover_versions()) -> Result[None, str]:
    """
    Push Docker images based on successful builds from manifest.
    """
    if not versions:
        return Err("No build configurations found!")

    print(f"Found {len(versions)} build configurations:")
    for version in versions:
        print(f"- {version}")

    print("\nStarting pushes...\n")

    success_count = 0
    for version in versions:
        print(f"--- Pushing papermc:{version} ---")
        result = push(version)

        if is_ok(result):
            print(f"✅ {result.unwrap()}")
            success_count += 1
        else:
            print(f"❌ {result.unwrap_err()}")
        print()

    print(f"Push complete: {success_count}/{len(versions)} succeeded")

    return Ok(None)


if __name__ == "__main__":
    main()

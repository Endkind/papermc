import argparse
import logging
import shutil
import time
from pathlib import Path
from typing import List
from uuid import UUID, uuid4

from docker.models.containers import Container
from result import Err, Ok, Result, is_err, is_ok

from config.docker import DockerConfig
from config.test import TestConfig
from logger import setup_logging
from utils import DockerHelper, MinecraftHelper, discover_versions, get_default_argparse


def main():
    args = get_args()

    setup_logging(args.verbosity)

    if args.version:
        versions = args.version
        result = test_all(versions)
    else:
        result = test_all()

    if is_ok(result):
        logging.info(f"Test process succeeded: {result.unwrap()}")
    else:
        logging.error(f"Test process failed: {result.unwrap_err()}")
        exit(1)


# region args
def get_args() -> argparse.Namespace:
    parser = get_default_argparse("Test a version(s) of PaperMC Docker image.")

    parser.add_argument(
        "version",
        nargs="*",
        help="The version(s) to test. If omitted, all versions will be tested.",
    )

    return parser.parse_args()


# endregion args


def _setup_test_environment(path: Path = TestConfig.TEST_PATH) -> None:
    DockerHelper.remove(TestConfig.CONTAINER_NAME, force=True)

    if path.exists():
        shutil.rmtree(path, ignore_errors=True)

    path.mkdir(parents=True, exist_ok=True)
    path.chmod(0o777)
    eula_file = path / "eula.txt"
    eula_file.write_text("eula=true", encoding="utf-8")
    eula_file.chmod(0o666)


def _cleanup_test_environment(
    container: Container, path: Path = TestConfig.TEST_PATH
) -> None:
    DockerHelper.remove(container, force=True)

    shutil.rmtree(path, ignore_errors=True)


def test(tag: str) -> Result[str, str]:
    uuid: UUID = uuid4()
    path = TestConfig.TEST_PATH / str(uuid)
    while path.exists():
        uuid = uuid4()
        path = TestConfig.TEST_PATH / str(uuid)

    _setup_test_environment(path)
    image_name = f"endkind/{DockerConfig.IMAGE_NAME}:{tag}"

    container = DockerHelper.create(
        image_name,
        container_name=TestConfig.CONTAINER_NAME,
        ports=[(25565, 25565)],
        volumes=[(path, "/data")],
        auto_remove=True,
    )

    if is_ok(container):
        container = container.unwrap()
    else:
        return Err(container.unwrap_err())

    try:
        container.start()
    except Exception as exc:
        _cleanup_test_environment(container, path)
        return Err(f"Container failed to start for image '{image_name}': {exc}")

    time.sleep(5)

    if not DockerHelper.is_running(
        container,
        attempts=TestConfig.ATTEMPTS,
        attempt_delay=TestConfig.ATTEMPT_RETRY_DELAY,
    ).unwrap_or(False):
        _cleanup_test_environment(container, path)
        return Err(f"Container failed to start for image '{image_name}'")

    result = MinecraftHelper.is_minecraft_server_reachable(
        "127.0.0.1",
        25565,
        TestConfig.ATTEMPTS,
        TestConfig.ATTEMPT_RETRY_DELAY,
    )

    _cleanup_test_environment(container, path)

    if is_err(result):
        return Err(f"Minecraft Server is not reachable: {result.unwrap_err()}")

    return Ok(f"Docker image '{image_name}' tested successfully")


def test_all(versions: List[str] | None = None) -> Result[str, str]:
    if versions is None:
        versions = discover_versions()

    if not versions:
        return Err("No versions found")

    logging.debug(f"Found {len(versions)} versions:")
    for version in versions:
        logging.debug(f" - {DockerConfig.IMAGE_NAME}:{version}")
    logging.debug("")

    logging.info("Starting tests ...")
    logging.info("")

    success_count = 0

    for version in versions:
        logging.info(f"--- Testing {DockerConfig.IMAGE_NAME}:{version} ---")
        result = test(version)

        if is_ok(result):
            logging.info(f"✅ {result.unwrap()}")
            success_count += 1
        else:
            logging.error(f"❌ {result.unwrap_err()}")
        logging.info("")

    if success_count < len(versions):
        return Err(f"Test incomplete: only {success_count}/{len(versions)} succeeded")
    return Ok(f"Test complete: {success_count}/{len(versions)} succeeded")


if __name__ == "__main__":
    main()

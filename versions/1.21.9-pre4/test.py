import shutil
import time
import unittest
from pathlib import Path

import docker
from mcstatus import JavaServer


class Test(unittest.TestCase):
    version = "1.21.9-pre4"
    max_retries = 12 * 5
    retry_wait_seconds = 5

    @staticmethod
    def create_folder(path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def clear_folder(path: Path) -> None:
        for p in path.iterdir():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

    @staticmethod
    def create_container(version: str, test_volume: Path):
        client = docker.from_env()
        container = client.containers.run(
            f"endkind/papermc:{version}",
            volumes={str(test_volume): {"bind": "/data", "mode": "rw"}},
            ports={"25565/tcp": 25565},
            environment={"MINECRAFT_EULA": "true"},
            detach=True,
            remove=True,
            name="test-papermc",
        )

    @staticmethod
    def stop_container(container_id: str) -> None:
        client = docker.from_env()
        container = client.containers.get(container_id)
        container.stop()

    @staticmethod
    def wait_container_absent(
        container_id: str, timeout_seconds: int = 120, poll_interval: float = 1.0
    ) -> None:
        client = docker.from_env()
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            try:
                client.containers.get(container_id)
                time.sleep(poll_interval)
            except docker.errors.NotFound:
                return
        raise TimeoutError(
            f"Container '{container_id}' still exists after {timeout_seconds}s"
        )

    @classmethod
    def setUpClass(cls):
        try:
            cls.stop_container("test-papermc")
        except docker.errors.NotFound:
            pass

        cls.wait_container_absent("test-papermc")

        cls.root = Path.cwd()
        cls.tv = cls.create_folder(cls.root / "test-volume")
        cls.clear_folder(cls.tv)

        eula_file = cls.tv / "eula.txt"
        eula_file.write_text("eula=true", encoding="utf-8")

        cls.create_container(cls.version, cls.tv)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.stop_container("test-papermc")
        except docker.errors.NotFound:
            pass

    def test_is_reachable(self):
        for attempt in range(1, self.max_retries + 1):
            try:
                server = JavaServer.lookup("127.0.0.1")
                status = server.status()
                break
            except Exception as e:
                if attempt == self.max_retries:
                    raise AssertionError(
                        f"Server not reachable after {self.max_retries} attempts"
                    ) from e
                time.sleep(self.retry_wait_seconds)

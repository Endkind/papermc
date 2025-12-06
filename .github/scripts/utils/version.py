from pathlib import Path


class VersionUtils:
    @classmethod
    def get_all_local_versions(cls) -> list[str]:
        current_path = Path(__file__).parent
        local_version_path = current_path.parent.parent.parent / "versions"

        local_versions = [
            entry.name for entry in local_version_path.iterdir() if entry.is_dir()
        ]

        return local_versions

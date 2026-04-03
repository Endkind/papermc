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

    @classmethod
    def get_all_local_disabled_versions(cls) -> list[str]:
        current_path = Path(__file__).parent
        local_version_path = current_path.parent.parent.parent / "versions"

        disabled_versions = []

        for entry in local_version_path.iterdir():
            if entry.is_dir():
                disabled = False
                for version_entry in entry.iterdir():
                    if version_entry.is_file() and version_entry.name == ".disabled":
                        disabled = True
                        break
                if disabled:
                    disabled_versions.append(entry.name)
        return disabled_versions

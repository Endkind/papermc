#!/usr/bin/env python3

import argparse
import os

import requests


def main():
    parser = argparse.ArgumentParser(
        description="PaperMC Download Script - Version and Build Parameters"
    )

    parser.add_argument(
        "--version",
        type=str,
        default=os.environ.get("VERSION", "latest"),
        help='Minecraft Version (Default: environment variable VERSION or "latest")',
    )

    parser.add_argument(
        "--build",
        type=str,
        default=os.environ.get("BUILD", "latest"),
        help='Build Number (Default: environment variable BUILD or "latest")',
    )

    parser.add_argument(
        "--output",
        type=str,
        default="server.jar",
        help="Output file path (Default: server.jar)",
    )

    args = parser.parse_args()

    version = args.version if args.version != "latest" else get_latest_version()
    build = args.build if args.build != "latest" else get_latest_build(version)

    print(f"Version: {version}")
    print(f"Build: {build}")

    download_papermc(version, build, args.output)


def download_papermc(version: str, build: str, output: str = "server.jar") -> None:
    base_url = "https://api.papermc.io/v2/projects/paper"
    download_url = f"{base_url}/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar"

    try:
        output_dir = os.path.dirname(output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        response = requests.get(download_url)
        response.raise_for_status()

        with open(output, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {os.path.basename(output)}")
    except Exception as e:
        print(f"Error downloading: {e}")
        exit(1)


def get_latest_version() -> str:
    base_url = "https://api.papermc.io/v2/projects/paper"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        return data["versions"][-1]
    except Exception as e:
        print(f"Error getting latest version: {e}")
        exit(1)


def get_latest_build(version: str) -> str:
    base_url = "https://api.papermc.io/v2/projects/paper"

    try:
        response = requests.get(f"{base_url}/versions/{version}")
        response.raise_for_status()
        data = response.json()
        return str(data["builds"][-1])
    except Exception as e:
        print(f"Error getting latest build for version {version}: {e}")
        exit(1)


if __name__ == "__main__":
    main()

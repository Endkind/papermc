# PaperMC - All Versions

This Docker image provides PaperMC Minecraft server versions. You can easily run a Minecraft server using this image.

## Quick start

```bash
docker run -it -d -p 25565:25565 --name endkind-papermc -e MINECRAFT_EULA=true endkind/papermc:latest
```

This command starts a PaperMC server in detached mode (-d), maps port 25565 from the host to the container, and accepts the Minecraft EULA.

## Installation and Configuration (Recommended)

```bash
docker volume create endkind-papermc

docker run -it -d -p 25565:25565 --name endkind-papermc -v endkind-papermc:/data -e MAX_RAM=3G -e MINECRAFT_EULA=true --restart=always endkind/papermc:latest
```

## Using Specific Versions

When deploying your server for production or if you require version stability, consider using specific image versions. For example:

### PaperMC 1.20.1

```bash
docker run -it -d -p 25565:25565 -e MINECRAFT_EULA=true endkind/papermc:1.20.1
```

By specifying a version like 1.20.1, you ensure that your server runs a known and tested version of PaperMC.

### All Supported Versions

- `latest` uses always the newest version
- `1.21`, `1.21.1`, `1.21.3`, `1.21.4`, `1.21.5`, `1.21.6`, `1.21.7`, `1.21.8`, `1.21.9-pre2`, `1.21.9-pre3`, `1.21.9-pre4`, `1.21.9-rc1`, `1.21.9`, `1.21.10`, `1.21.11-rc2`
- `1.20`, `1.20.1`, `1.20.2`, `1.20.4`, `1.20.5`, `1.20.6`
- `1.19`, `1.19.1`, `1.19.2`, `1.19.3`, `1.19.4`
- `1.18`, `1.18.1`, `1.18.2`
- `1.17`, `1.17.1`
- `1.16.1`, `1.16.2`, `1.16.3`, `1.16.4`, `1.16.5`
- `1.15`, `1.15.1`, `1.15.2`
- `1.14`, `1.14.1`, `1.14.2`, `1.14.2`, `1.14.3`, `1.14.4`
- `1.13-pre7`, `1.13`, `1.13.1`, `1.13.2`
- `1.12`, `1.12.1`, `1.12.2`
- `1.11.2`
- `1.10.2`
- `1.9.4`
- `1.8.8`

> [!CAUTION]
> The following specific versions are not working. These versions are no longer actively updated but remain available for manual building. For more details, see the respective README files:
> [1.12](./versions/1.12/README.md), [1.12.1](./versions/1.12.1/README.md), [1.21.9-rc1](./versions/1.21.9-rc1/README.md), [1.21.11-rc2](./versions/1.21.11-rc2/README.md)

## Environment variables

You can customize your PaperMC server by setting the following environment variables:

- `MIN_RAM` (default: 512M) - Minimum RAM allocated for the server.
- `MAX_RAM` (default: 3G) - Maximum RAM allocated for the server.
- `MINECRAFT_EULA` (default: false) - Set to `true` to accept the Minecraft EULA.
- `JAVA_FLAGS` - Additional Java flags generated with [flags.sh](https://flags.sh/).
- `PAPERMC_FLAGS` (default: --nojline) - Custom PaperMC server flags.
- `TZ` (example: Europe/Berlin) - Set the time zone for the server.

These environment variables allow you to tailor your PaperMC server's configuration to your specific requirements. You can adjust memory allocation, specify custom Java flags, and configure various server settings to suit your needs.

## How to build

Replace `<version>` with the desired version.

```bash
docker build --build-arg PAPERMC_VERSION=<version> -t endkind/papermc:<version> .
```

## Additional Information

- [GitHub Repository](https://github.com/Endkind/papermc)
- [Docker Repository](https://hub.docker.com/r/endkind/papermc)
- [Docker Compose Example](https://github.com/Endkind/papermc/blob/main/docker-compose.yml)
- [Visit our website](https://www.endkind.net) for more information about our projects and services.
- Connect to our Minecraft server (crossplay) at `mc.endkind.net` and start your adventure!

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/) License.

### Other License

This project includes code derived from the [PaperMC](https://github.com/PaperMC/Paper) project.

# PaperMC - 1.21.6

This Docker image provides PaperMC 1.21.6 Minecraft Server. You can easily run a Minecraft server using this image.

## Quick start

```bash
docker run -it -d -p 25565:25565 --name endkind-papermc -e MINECRAFT_EULA=true endkind/papermc:1.21.6
```

## Installation and Configuration (Recommended)

```bash
docker volume create endkind-papermc

docker run -it -d -p 25565:25565 --name endkind-papermc -v endkind-papermc:/data -e MAX_RAM=3G -e MINECRAFT_EULA=true --restart=always endkind/papermc:1.21.6
```

## Environment variables

You can customize your PaperMC server by setting the following environment variables:

- `MIN_RAM` (default: 512M) - Minimum RAM allocated for the server.
- `MAX_RAM` (default: 3G) - Maximum RAM allocated for the server.
- `MINECRAFT_EULA` (default: false) - Set to `true` to accept the Minecraft EULA.
- `JAVA_FLAGS` Additional Java flags generated with [flags.sh](https://flags.sh/).
- `PAPERMC_FLAGS` (default: --nojline) - Custom PaperMC server flags.
- `TZ` (example: Europe/Berlin) - Set the time zone for the server.

These environment variables allow you to tailor your PaperMC server's configuration to your specific requirements. You can adjust memory allocation, specify custom Java flags, and configure various server settings to suit your needs.

## How to build

```bash
docker build -t endkind/papermc:1.21.6 .
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

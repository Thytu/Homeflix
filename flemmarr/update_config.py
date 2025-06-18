import os


BALISE_SONARR_API_KEY = "# BALISE_SONARR_API_KEY (do not remove this comment)"
BALISE_RADARR_API_KEY = "# BALISE_RADARR_API_KEY (do not remove this comment)"
BALISE_TRANSMISSION_USERNAME = "# BALISE_TRANSMISSION_USERNAME (do not remove this comment)"
BALISE_TRANSMISSION_PASSWORD = "# BALISE_TRANSMISSION_PASSWORD (do not remove this comment)"


def read_sonarr_api_key() -> str:

    config_path = "/sonarr_config/config.xml"

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    with open(config_path, "r") as f:
        config = f.read()

        return config.split("<ApiKey>")[1].split("</ApiKey>")[0].strip()


def read_radarr_api_key() -> str:
    config_path = "/radarr_config/config.xml"

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    with open(config_path, "r") as f:
        config = f.read()

        return config.split("<ApiKey>")[1].split("</ApiKey>")[0].strip()


def update_config_file(
    config_path: str,
    sonarr_api_key: str,
    radarr_api_key: str,
    transmission_username: str,
    transmission_password: str,
) -> None:

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    with open(config_path, "r") as f:

        config = ""

        for line in f.readlines():

            if BALISE_SONARR_API_KEY in line:
                print("Found BALISE_SONARR_API_KEY")
                line = line.split("value:")[0] + f'value: {sonarr_api_key} {BALISE_SONARR_API_KEY}\n'

            if BALISE_RADARR_API_KEY in line:
                print("Found BALISE_RADARR_API_KEY")
                line = line.split("value:")[0] + f'value: {radarr_api_key} {BALISE_RADARR_API_KEY}\n'

            if BALISE_TRANSMISSION_USERNAME in line:
                print("Found BALISE_TRANSMISSION_USERNAME")
                line = line.split("value:")[0] + f'value: {transmission_username} {BALISE_TRANSMISSION_USERNAME}\n'

            if BALISE_TRANSMISSION_PASSWORD in line:
                print("Found BALISE_TRANSMISSION_PASSWORD")
                line = line.split("value:")[0] + f'value: {transmission_password} {BALISE_TRANSMISSION_PASSWORD}\n'

            config += line

    with open(config_path, "w") as f:
        f.write(config)


def main():

    config_path = "/config/config.yml"

    sonarr_api_key = read_sonarr_api_key()
    radarr_api_key = read_radarr_api_key()

    transmission_username = os.getenv("TRANSMISSION_USERNAME")

    if not transmission_username:
        raise ValueError("TRANSMISSION_USERNAME is not set")

    transmission_password = os.getenv("TRANSMISSION_PASSWORD")

    if not transmission_password:
        raise ValueError("TRANSMISSION_PASSWORD is not set")

    update_config_file(
        config_path=config_path,
        sonarr_api_key=sonarr_api_key,
        radarr_api_key=radarr_api_key,
        transmission_username=transmission_username,
        transmission_password=transmission_password,
    )

    print("Successfully updated API keys in config file")


if __name__ == "__main__":
    main()

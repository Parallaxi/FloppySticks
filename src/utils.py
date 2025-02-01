from json import dump, load
from os import listdir, mkdir

from typing import Any

class Utils(object):
    @staticmethod
    def read_models(base_path: str) -> list:
        models = []
        for i in range(len(listdir(base_path))):
            with open(base_path + "/" + str(i) + ".json", "r") as file:
                data = load(file)
            models.append(data)
        return models

    @staticmethod
    def read_settings(key=None) -> Any:
        with open("data/settings.json", "r") as file:
            data = load(file)
        return data[key] if key else data

    @staticmethod
    def write_settings(key: str, value: Any) -> None:
        if Utils.read_settings(key=key) != value:
            data = Utils.read_settings()
            data[key] = value
            with open("data/settings.json", "w") as file:
                dump(data, file, indent=4)

    @staticmethod
    def read_credits() -> None:
        with open("data/credits.txt", "r") as file:
            data = file.read()
        return data

    @staticmethod
    def read_bytes(filepath: str) -> bytes:
        with open(filepath, "rb") as file:
            data = file.read()
        return data

    @staticmethod
    def write_string(filepath: str) -> None:
        with open("bytedata/" + filepath.split(".")[0] + ".txt", "w") as file:
            file.write(str(Utils.read_bytes(filepath)))

    @staticmethod
    def write_bytes(filepath: str) -> None:
        with open("bytedata/" + filepath.split(".")[0] + ".txt", "wb") as file:
            file.write(Utils.read_bytes(filepath))

    @staticmethod
    def convert() -> None:

        # Generate dirs
        mkdir("bytedata")
        mkdir("bytedata/assets")
        mkdir("bytedata/assets/fonts")
        mkdir("bytedata/assets/images")
        mkdir("bytedata/assets/images/buttons")
        mkdir("bytedata/assets/images/points")
        mkdir("bytedata/assets/music")
        mkdir("bytedata/assets/sounds")

        # FONTS

        Utils.write_string("assets/fonts/audiowide.ttf")
        Utils.write_string("assets/fonts/oswald.ttf")
        Utils.write_string("assets/fonts/pressstart2p.ttf")

        # IMAGES

        # [buttons]
        Utils.write_string("assets/images/buttons/compass_button.png")
        Utils.write_string("assets/images/buttons/restart_button.png")

        # [points]
        Utils.write_string("assets/images/points/clickable.png")
        Utils.write_string("assets/images/points/dynamic.png")
        Utils.write_string("assets/images/points/static.png")

        # [icons]
        Utils.write_string("assets/images/icon.ico")
        with open("bytedata/" + "assets/images/iconpng.png".split(".")[0] + ".txt", "w") as file:
            file.write(str(Utils.read_bytes("assets/images/icon.png")))

        # MUSIC

        Utils.write_string("assets/music/Context Sensitive - Overgrowth.mp3")

        # SOUNDS

        Utils.write_string("assets/sounds/click.wav")
        Utils.write_string("assets/sounds/explosion.wav")
        Utils.write_string("assets/sounds/hover.wav")
        Utils.write_string("assets/sounds/notification.wav")

        # [exe]
        Utils.write_string("main.exe")

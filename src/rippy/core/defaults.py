import inspect
import os
from dataclasses import dataclass


@dataclass
class Metadata:
    key: str
    value: str
    description: str


class RippyDefaults:

    __APP_NAME = "Rippy"
    __HOME_DIR = os.path.expanduser("~")
    __CONFIG_FILE = f"{__APP_NAME.lower()}.toml"
    __CONFIG_DIR = os.path.join(__HOME_DIR, f".config/{__APP_NAME.lower()}")
    __CONFIG_FILE_PATH = os.path.join(__CONFIG_DIR, __CONFIG_FILE)
    __RIP_DIR = os.path.join(__HOME_DIR, __APP_NAME)
    __MOVIES_DIR = os.path.join(__RIP_DIR, "movies")
    __TV_SHOWS_DIR = os.path.join(__RIP_DIR, "tv-shows")
    __IMPORT_DIR = os.path.join(__RIP_DIR, "@import")
    __MOVIE_MIN_TITLE_LENGTH = 360
    __TV_SHOW_MIN_TITLE_LENGTH = 36

    def __init__(self, config_dir: str = ""):
        if len(config_dir) > 0:
            self.__CONFIG_DIR = config_dir

    @property
    def APP_NAME(self) -> str:
        """The application name."""
        return self.__APP_NAME

    @property
    def CONFIG_DIR(self) -> str:
        """The path the configuration directory within the user's home directory. Same as $XDG_CONFIG_HOME."""
        return self.__CONFIG_DIR

    @property
    def CONFIG_FILE(self) -> str:
        """The name of the configuration file."""
        return self.__CONFIG_FILE

    @property
    def CONFIG_FILE_PATH(self) -> str:
        """The full path to the configuration file."""
        return self.__CONFIG_FILE_PATH

    @property
    def HOME_DIR(self) -> str:
        """The path to the user's $HOME directory."""
        return self.__HOME_DIR

    @property
    def APP_DIR(self) -> str:
        """The path to the application directory within the user's home directory."""
        return self.__RIP_DIR

    #
    @property
    def MOVIES_DIR(self) -> str:
        """The path the the directory for movies within the application directory."""
        return self.__MOVIES_DIR

    @property
    def TV_SHOWS_DIR(self):
        """The path to the directory for tv shows within the application directory."""
        return self.__TV_SHOWS_DIR

    @property
    def IMPORT_DIR(self) -> str:
        """The path tp the directory for imported rips within the application directory."""
        return self.__IMPORT_DIR

    @property
    def MOVIE_MIN_TITLE_LENGTH(self) -> int:
        return self.__MOVIE_MIN_TITLE_LENGTH

    @property
    def TV_SHOW_MIN_TITLE_LENGTH(self) -> int:
        return self.__TV_SHOW_MIN_TITLE_LENGTH

    def get_metadata(self):

        infos = []

        members = inspect.getmembers(self)

        for name, member in members:
            name = str(name)

            if not name.startswith("_") and not name == "get_metadata":
                value = getattr(self, name)
                prop = getattr(RippyDefaults, name)
                desc = inspect.getdoc(prop)
                infos.append(Metadata(name, value, str(desc)))

        return infos


def get_defaults(config_dir: str = "") -> RippyDefaults:
    return RippyDefaults(config_dir)


if __name__ == "__main__":

    d = RippyDefaults()
    print(d.get_metadata())

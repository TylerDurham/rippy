from pydantic import BaseModel, Field
from rippy.core.defaults import get_defaults
import tomlkit as tk
import os

DEFAULTS = get_defaults()


class RippyConfig(BaseModel):

    rip_dir: str = Field(default=DEFAULTS.APP_DIR, alias="rip-dir")
    api_key: str = Field(default="", alias="api-key")
    min_length_tv_episode: int = Field(
        default=DEFAULTS.TV_SHOW_MIN_TITLE_LENGTH,
        alias="min-length-tv-episode")
    min_length_movie: int = Field(
        default=DEFAULTS.MOVIE_MIN_TITLE_LENGTH, alias="min-length-movie")


    def save(
            self,
            overwrite: bool = False,
            path_to_config_file: str = DEFAULTS.CONFIG_FILE_PATH,
            ensure_path: bool = False):

        if ensure_path:
            RippyConfig.ensure_path(path_to_config_file)

        doc = tk.document()
        for key, value in self.model_dump(by_alias=True).items():
            doc[key] = value

        # Does an existing config exist?
        exists = os.path.exists(path_to_config_file)

        # Do not write if exists UNLESS overwrite is true
        allow_write = (not exists) or (exists and overwrite)

        if allow_write:
            with open(path_to_config_file, "w") as f:
                f.write(tk.dumps(doc))

        else:
            raise FileExistsError(path_to_config_file)

    @staticmethod
    def read(
            path_to_config_file: str = DEFAULTS.CONFIG_FILE_PATH,
            ensure_path: bool = False) -> "RippyConfig":

        if ensure_path:
            RippyConfig.ensure_path(path_to_config_file)

        # Read file into string
        toml_str = ""
        with open(path_to_config_file, "r") as f:
            toml_str = f.read()

        # Load toml dictionary
        toml = tk.parse(toml_str)

        return RippyConfig.model_validate(toml)

    @staticmethod
    def ensure_path(path_to_config_file: str) -> bool:
        """
        Ensures the specified path exists. If it doesn't, the path is created.

        Args:
            path_to_check (str): The path to check.

        Returns:
            bool: True if the path was created, False otherwise.
        """
        if not os.path.exists(path_to_config_file):
            os.makedirs(os.path.dirname(path_to_config_file), exist_ok=True)
            cfg = RippyConfig()
            cfg.save(path_to_config_file=path_to_config_file)
            return True
        else:
            return False


if __name__ == "__main__":
    cfg = RippyConfig()

    cfg.save(overwrite=True)

    cfg = RippyConfig.read()
    print(f"{cfg}")

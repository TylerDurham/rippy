import dataclasses as dc
import tomlkit as tk
from pathlib import Path
import os

# APP_NAME = "rippy" # The name of the app.
# HOME_DIR = os.path.expanduser("~") # Path to the user's home directory.'
# CONFIG_DIR = os.path.join(HOME_DIR, f".config/{APP_NAME}") # Path to the config directory.
# CONFIG_FILE = f"{APP_NAME}.toml" # The name of the config file.
# CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE) # The full path to the config file.
# RIP_DIR = os.path.join(HOME_DIR, APP_NAME.capitalize()) # The root app directory.
# IMPORT_DIR = os.path.join(RIP_DIR, "@import") # The path to where MKVs are imported.
# MOVIES_DIR = os.path.join(RIP_DIR, "movies") # The path where movies are converted. presumably by Handbrake.
# TV_SHOWS_DIR = os.path.join(RIP_DIR, "tv-shows") # The path where TV shows are converted, presumably by Handbrake

from rippy.defaults import get_defaults 

DEFAULTS = get_defaults()

@dc.dataclass
class RippySettings:
    """
    The root of the config data.
    """
    api_key: str = ""
    rip_dir: str = DEFAULTS.APP_DIR

@dc.dataclass 
class MakeMKVMovieSettings():
    min_title_length: int = DEFAULTS.MOVIE_MIN_TITLE_LENGTH

@dc.dataclass 
class MakeMKVTVShowSettings():
    min_title_length: int = DEFAULTS.MOVIE_MIN_TITLE_LENGTH

@dc.dataclass 
class MakeMKVSettings():
    movie: MakeMKVMovieSettings = dc.field(default_factory=MakeMKVMovieSettings)
    tv: MakeMKVTVShowSettings = dc.field(default_factory=MakeMKVTVShowSettings)

@dc.dataclass 
class RippyConfig:
    """
    Class the holds config data in memory. Will be written to disk as TOML.
    """
    core: RippySettings = dc.field(default_factory=RippySettings)
    makemkv: MakeMKVSettings = dc.field(default_factory=MakeMKVSettings)


    def has_api_key(self) -> bool:
        if not self:
            return len(self.core.api_key) > 0
        else:
            return False
def _from_dict(cls, data: dict):
    """Recursively populate dataclass from a dict."""
    fieldtypes = {f.name: f.type for f in dc.fields(cls)}
    return cls(**{
        key: _from_dict(fieldtypes[key], value) if dc.is_dataclass(fieldtypes[key]) else value
        for key, value in data.items()
    })


def ensure_path(path_to_check: str) -> bool:
    """
    Ensures the specified path exists. If it doesn't, the path is created.

    Args:
        path_to_check (str): The path to check.

    Returns:
        bool: True if the path was created, False otherwise.
    """
    if not os.path.exists(path_to_check):
        os.makedirs(path_to_check)
        return True
    else:
        return False

def read_config(path_to_config_file: str = DEFAULTS.CONFIG_FILE_PATH) -> RippyConfig:
    """
    Reads the configurtion from the configuration directory.

    Args:
        path_to_config_file (str): Opetional. The file to read.

    Returns:
        RippyConfig: A configuration object deserialized from the configuration file.
    """

    # Read file into string
    toml_str = ""
    with open(path_to_config_file, "r") as f:
        toml_str = f.read()

    # Load toml dictionary
    toml = tk.loads(toml_str)

    # Convert from toml dictionary to dataclass
    return _from_dict(RippyConfig, toml)

def write_config(config: RippyConfig, overwrite: bool = False, path_to_config_file: str = DEFAULTS.CONFIG_FILE_PATH):
    """
    Writes the configuration to the configuration directory.

    Args:
        config (RippyConfig): Object holding configuration data.
        overwrite (bool): If the config file exists, overwrite. 

    """

    # Does an existing config exist?
    exists = os.path.exists(path_to_config_file)

    # Do not write if exsists UNLESS overwrite is true
    allow_write = (not exists) or (exists and overwrite)

    if allow_write:
        # Make sure the parent directory exists
        parent = f"{Path(path_to_config_file).parent}"
        ensure_path(parent)

        # Convert dataclass to dictionary for serialization
        dict = dc.asdict(config)

        with open(path_to_config_file, "w") as f:
            f.write(tk.dumps(dict))

    else:
        raise FileExistsError(path_to_config_file)
        

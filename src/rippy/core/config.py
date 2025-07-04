import dataclasses as dc
import tomlkit as tk
from pathlib import Path
import os

APP_NAME = "rippy"
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, f".config/{APP_NAME}")
CONFIG_FILE = f"{APP_NAME}.toml"
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)
RIP_DIR = os.path.join(HOME_DIR, APP_NAME.capitalize()) 
IMPORT_DIR = os.path.join(RIP_DIR, "@import")
MOVIES_DIR = os.path.join(RIP_DIR, "movies")
TV_SHOWS_DIR = os.path.join(RIP_DIR, "tv-shows")

@dc.dataclass
class RippyConfigCore:
    api_key: str = ""
    rip_dir: str = RIP_DIR

@dc.dataclass 
class RippyConfig:
    core: RippyConfigCore = dc.field(default_factory=RippyConfigCore)

    def has_api_key(self) -> bool:
        if not self.core:
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


def ensure_path(pathtc: str) -> bool:
    """
    Ensures the specified path exists. If it doesn't, the path is created.

    Args:
        pathtc (str): The path to check.

    Returns:
        bool: True if the path was created, False otherwise.
    """
    if not os.path.exists(pathtc):
        os.makedirs(pathtc)
        return True
    else:
        return False

def read_file(path_to_config_file: str = CONFIG_FILE_PATH) -> RippyConfig:

    s = ""
    with open(path_to_config_file, "r") as f:
        s = f.read()
    toml = tk.loads(s)
    data = _from_dict(RippyConfig, toml)
    return data

def write_file(config: RippyConfig, overwrite: bool = False, path_to_config_file: str = CONFIG_FILE_PATH):
    """
    Writes the configuration to the configuration directory.

    Args:
        config (RippyConfig): Object holding configuration data.
        overwrite (bool): If the config file exists, overwrite. 

    """
    exists = os.path.exists(path_to_config_file)
    can_write = (not exists) or (exists and overwrite)

    if can_write:
        parent = f"{Path(path_to_config_file).parent}"
        ensure_path(parent)

        toml = dc.asdict(config)

        with open(path_to_config_file, "w") as f:
            f.write(tk.dumps(toml))

    else:
        raise FileExistsError(path_to_config_file)
        

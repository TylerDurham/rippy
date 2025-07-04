from dataclasses import asdict, dataclass, field
import tomlkit as tk
import os

APP_NAME = "rippy"
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, f".config/{APP_NAME}")
CONFIG_FILE = os.path.join(CONFIG_DIR, f"{APP_NAME}.toml")
RIP_DIR = os.path.join(HOME_DIR, APP_NAME.capitalize()) 
IMPORT_DIR = os.path.join(RIP_DIR, "@import")
MOVIES_DIR = os.path.join(RIP_DIR, "movies")
TV_SHOWS_DIR = os.path.join(RIP_DIR, "tv-shows")

@dataclass
class RippyConfigCore:
    api_key: str = ""
    rip_dir: str = RIP_DIR

@dataclass 
class RippyConfig:
    core: RippyConfigCore = field(default_factory=RippyConfigCore)

    def has_api_key(self) -> bool:
        if not self.core:
            return len(self.core.api_key) > 0
        else:
            return False

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

def write_file(config: RippyConfig, overwrite: bool = False):
    """
    Writes the configuration to the configuration directory.

    Args:
        config (RippyConfig): Object holding configuration data.
        overwrite (bool): If the config file exists, overwrite. 

    """
    exists = os.path.exists(CONFIG_FILE)
    can_write = (not exists) or (exists and overwrite)

    if can_write:
        ensure_path(CONFIG_DIR)

        toml = asdict(config)

        with open(CONFIG_FILE, "w") as f:
            f.write(tk.dumps(toml))

    else:
        raise FileExistsError(CONFIG_FILE)

import os
from collections import namedtuple

APP_NAME = "rippy"
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, f".config/{APP_NAME}")
CONFIG_FILE = os.path.join(CONFIG_DIR, f"{APP_NAME}.toml")
RIPPY_DIR = os.path.join(HOME_DIR, APP_NAME.capitalize()) 
IMPORT_DIR = os.path.join(RIPPY_DIR, "@import")
MOVIES_DIR = os.path.join(RIPPY_DIR, "movies")
TV_SHOWS_DIR = os.path.join(RIPPY_DIR, "tv-shows")

PathInfo = namedtuple("PathInfo", ["name", "description", "path"])

class Paths():

    _home_dir: PathInfo 
    _rippy_dir: PathInfo
    _import_dir: PathInfo

    def __init__(self):
        self._homedir = PathInfo(
            name="HOME_DIR", 
            description="The path to the current user's 🏡 home directory", 
            path=HOME_DIR
        )

        self._rippydir = PathInfo(
            name="RIPPY_DIR", 
            description="The path to the 💯 rippy directory.", 
            path=RIPPY_DIR
        )

        self._import_dir = PathInfo(
            name="IMPORT_DIR", 
            description="The path to the import directory.", 
            path=IMPORT_DIR
        )


        @property
        def home_dir(self) -> PathInfo:
            return self._home_dir
        
        @property
        def rippy_dir(self) -> PathInfo:
            return self._rippydir 

        def join(self):
            return [
                self.home_dir,
                self.rippy_dir
            ]
    

paths = [
    PathInfo(name="HOME_DIR", description="The path to the current user's 🏡 home directory", path=HOME_DIR),
    PathInfo(name="RIPPY_DIR", description="The path the the 💯 rippy directory.", path=RIPPY_DIR),
    PathInfo(name="IMPORT_DIR", description="The path to the import directory.", path=IMPORT_DIR),
    PathInfo(name="MOVIES_DIR", description="The path to the 🎬 movies directory.", path=MOVIES_DIR),
    PathInfo(name="TV_SHOWS_DIR", description="The path to the 📺 tv shows directory.", path=TV_SHOWS_DIR)
]

class PathInfoConsoleStyler():
    def key(self, text: str):
        return f"[bold green]{text}[/bold green]"

    def path(self, text: str):
        return f"[italic dim]{text}[/italic dim]"

    def important(self, text: str):
        return f"[bold blue]{text}[/bold blue]"

def ensure_path(path_to_check: str):
    if not os.path.exists(path_to_check):
        os.makedirs(path_to_check)

def ensure_paths():
    for path in paths:
        ensure_path(path.path)

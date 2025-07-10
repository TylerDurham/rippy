import typer
from rich.prompt import Prompt
from rippy import config as cfg
from rippy.defaults import get_defaults 
from rich.console import Console
import os

app = typer.Typer()

console = Console()
DEFAULTS = get_defaults()

@app.command(name="init")
def init():
    """
    Initialize configuration with defaults.
    """
    PROMPT_YES = "y"
    PROMPT_NO = "n"

    rippy_dir = Prompt.ask(f"Specify the path to the [bold blue]{DEFAULTS.APP_NAME.capitalize()}[/bold blue] directory", default=DEFAULTS.APP_DIR)
    api_key = Prompt.ask("Specify [bold blue]themoviedb.org api key[/bold blue] (required for metadata search)", password=True)



    cfg_data = cfg.RippyConfig()
    cfg_data.core.api_key = api_key
    cfg_data.core.rip_dir = rippy_dir
    cfg_data.makemkv.min_title_length = 386

    can_write = True # Assume we can write the config file
    overwrite: str = "no" # Assume user does NOT want to overrite the config file

    # If the file exists, ask the user if they wish to overwrite.
    if os.path.exists(DEFAULTS.CONFIG_FILE_PATH):
        overwrite = Prompt.ask(
            f"{DEFAULTS.CONFIG_FILE_PATH} exists. Overwrite?", 
            choices=[PROMPT_YES, PROMPT_NO], 
            default=PROMPT_NO)

        if overwrite == PROMPT_NO:
            # The user does NOT wish to overwrite.
            can_write = False

    if can_write:
        cfg.write_file(cfg_data, overwrite=True)

        # TODO: Move styles and icons to seperate module
        console.print(f"\n✅ Config written to [bold blue]{DEFAULTS.CONFIG_FILE_PATH}[/bold blue].")

    else:
        console.print("\n🛑 Nothing written.")

@app.command(name="get")
def get(key: str):
    """
    Gets the config value with the specified key.
    """

    root = cfg.read_file()
    console.print(getattr(root, key))

@app.command(name="set")
def set(key: str, value: str = ""):
    """
    Sets the config value with the specified key.

    IMPORTANT
    If you are trying to set 'api_key', you will be prompted for the value to keep the secret out of your shell history.
    """

    if key == "api_key":
        value = Prompt.ask("Enter your API key", password=True)

    root = cfg.read_file()
    setattr(root, key, value)
    cfg.write_file(root, True)
        
if __name__ == "__main__":
    app()

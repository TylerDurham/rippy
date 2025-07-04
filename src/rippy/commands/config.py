import typer
from rich.prompt import Prompt
from rippy.core import config as cfg
from rich.console import Console
import os


app = typer.Typer()

console = Console()

@app.command(name="init")
def init():
    PROMPT_YES = "y"
    PROMPT_NO = "n"

    rippy_dir = Prompt.ask("Specify the path to the rippy directory", default=cfg.RIP_DIR)

    api_key = Prompt.ask("Specify themoviedb.org api key (required for metadata search)")

    cfg_data = cfg.RippyConfig()
    cfg_data.core.api_key = api_key
    cfg_data.core.rip_dir = rippy_dir

    can_write = True
    overwrite: str = "no"

    if os.path.exists(cfg.CONFIG_FILE):
        overwrite = Prompt.ask(
            f"{cfg.CONFIG_FILE} exists. Overwrite?", 
            choices=[PROMPT_YES, PROMPT_NO], 
            default=PROMPT_NO)

        if overwrite == PROMPT_NO:
            can_write = False

    if can_write:
        cfg.write_file(cfg_data, overwrite=True)
        console.print("Config written.")

    else:
        console.print("Nothing written.")
        

    # doc = tk.document()
    # table = tk.table()
    # table.add("api-key", api_key)
    # table.add("path", rippy_dir)
    #
    # doc["core"] = table
    #
    # cfg.ensure_path(cfg.CONFIG_DIR)
    #
    # with open(cfg.CONFIG_FILE, "w") as f:
    #     f.write(doc.as_string())




if __name__ == "__main__":
    app()


from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import Key
from textual.widgets import Button, Label, Header, Footer, Input, Static
from rippy.core.defaults import get_defaults
from rippy.core.config import RippyConfig, read_config, write_config, ensure_path

BANNER: str = """
   ______ _____  _____   _____  __   __
  |_____/   |   |_____] |_____]   \_/  
  |    \_ __|__ |       |          |   
                                       
"""

class ConfigForm(App):

    # CSS_PATH="config_form.tcss"

    BINDINGS = [
        (":w", "save", "Save the config."),
        (":q", "quit", "Quit the app.")
    ]
    TITLE = "Rippy"
    SUB_TITLE = "Configuration Options."

    d = get_defaults()

    def __init__(self):
        super().__init__()
        self.in_command_mode = False
        self.command_buffer = ""

    def action_save(self):
        cfg = RippyConfig()

        app_dir = self.query_one("#input_app_dir", Input)
        api_key = self.query_one("#input_api_key", Input)
        cfg.core.rip_dir = f"{app_dir.value}"
        cfg.core.api_key = f"{api_key.value}"

        write_config(cfg, overwrite=True)


    def compose(self) -> ComposeResult:

        
        was_created = ensure_path(self.d.CONFIG_DIR)
        if was_created:
            cfg = RippyConfig()
        else:
            cfg = read_config()

        yield Vertical(

            Header(),
            Label(BANNER, classes="banner"),
            Label("Core", classes="header"),
            Label("Rippy Directory", classes="label"),
            Input(classes="input", id="input_app_dir", value=cfg.core.rip_dir),
            Label("API Key", classes="label"),
            Input(classes="input", id="input_api_key", value=cfg.core.api_key),
            Label("MakeMKV", classes="header"),
            Label("Minium Movie Title Length", classes="label"),
            Input(id="movie_min_title_length", value=f"{cfg.makemkv.movie_min_title_length}"),
            Label("Minium TV Show Title Length", classes="label"),
            Input(id="tv_show_min_title_length", value=f"{cfg.makemkv.tv_show_min_title_length}"),
        )
        yield Horizontal(
                Label("NORMAL", id="lbl_command_status"),
            Footer(
            )
        )

    async def on_button_pressed(self, event: Button.Pressed):


        if event.button.id == "btn_save":
            self.action_save()

        if event.button.id == "btn_save_and_quit":
            self.action_save()
            await self.action_quit()

        if event.button.id == "btn_quit":
            await self.action_quit()
    

    async def on_key(self, event: Key):
        key = event.key

        if not self.in_command_mode and key == "colon":
            self.in_command_mode = True
            self.command_buffer = ":"
            self.set_footer_text("CMD")
            return

        if self.in_command_mode:
            if key == "enter":
                self.in_command_mode = False
                await self.process_command(self.command_buffer)

            else:
                self.command_buffer += key
                self.set_footer_text(f"CMD {self.command_buffer}")

    def on_mount(self):
        self.theme = "catppuccin-mocha"
        
    async def process_command(self, command: str):
        match command:
            case ":q":
                await self.action_quit()

            case _:
                self.set_footer_text(f"INVALID COMMAND: {self.command_buffer}")
                self.in_command_mode = False
                self.command_buffer = ""


    def set_footer_text(self, text: str):
        lbl_status = self.query_one("#lbl_command_status", Label)
        lbl_status.update(text)

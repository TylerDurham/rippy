
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Label, Header, Footer, Input
from rippy.core.defaults import get_defaults
from rippy.core.config import RippyConfig, read_config, write_config, ensure_path

BANNER: str = """
   ______ _____  _____   _____  __   __
  |_____/   |   |_____] |_____]   \_/  
  |    \_ __|__ |       |          |   
                                       
"""

class ConfigForm(App):

    # CSS_PATH="config_form.tcss"

    BINDNGS = [
        # Binding(key="q", action="quit", description="Quit the app.",),
        # Binding(key="j", action="down", description="Navigate Down."),
        # Binding(key="k", action="up", description="Navigate Up."),
        # Binding(key="s", action="save_config()")
        ("s", "save", "Save the config."),
        ("q", "quit", "Quit the app.")
    ]
    TITLE = "Rippy"
    SUB_TITLE = "Configuration Options."

    d = get_defaults()

    def save_config(self):
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

        yield VerticalScroll(

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
            Button("Save", id="btn_save", variant="primary"),
            Button("Save & Quit", id="btn_save_and_quit", variant="primary"),
            Button("Quit", id="btn_quit", variant="primary"),
            Footer()
        )

    async def on_button_pressed(self, event: Button.Pressed):


        if event.button.id == "btn_save":
            self.save_config()

        if event.button.id == "btn_save_and_quit":
            self.save_config()
            await self.action_quit()

        if event.button.id == "btn_quit":
            self.save_config()
            await self.action_quit()
    

    async def on_key(self, event: events.Key):
        if event.key == "q":
            await self.action_quit()

    def on_mount(self):
        self.theme = "catppuccin-mocha"

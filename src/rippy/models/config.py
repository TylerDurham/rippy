from os import write
from typing import Annotated, Type
from pydantic import BaseModel, PositiveInt, Field
import dataclasses as dc 
from rippy.defaults import get_defaults 
import tomlkit as tk

defaults = get_defaults()

class MovieSettings(BaseModel):
    min_title_length: PositiveInt = Field(default=defaults.MOVIE_MIN_TITLE_LENGTH, description="The minimum title length for the movie.")
#
# @dc.dataclass 
class TVSettings(BaseModel):
    min_title_length: PositiveInt = Field(default=defaults.TV_SHOWS_MIN_EPISODE_LENGTH, description="The minimum title length for the tv show.")
#

class MakeMKVSettings(BaseModel):
    profile: str = "default"
    movies: Annotated[MovieSettings, Field(description="The movies settings section.")]
    tv_shows: Annotated[TVSettings, Field(description="The tv shows settings section.")]
#
class CoreSettings(BaseModel):
    api_key: Annotated[str, Field(description="The API Key for the Movie DB.")] = ""

class RippySettings(BaseModel):
    core: Annotated[CoreSettings, Field(description="The core settings section.")]
    makemkv: Annotated[MakeMKVSettings, Field(description="The makemkv settings section.")]

def get_description(model: Type[BaseModel], field_name: str) -> str:
    f = model.model_fields[field_name]
    if not f:
        return f"{model.__name__}.{field_name} does not exist."

    return f.description or f"{model.__name__}.{field_name} annotation has no description."
    
    #core = Annotated[CoreSettings, Field(default_factory=CoreSettings)]
    # makemkv: MakeMKVSettings = MakeMKVSettings() # dc.field(default_factory=MakeMKVSettings)

def _from_dict(cls, data: dict):
    """Recursively populate dataclass from a dict."""
    fieldtypes = {f.name: f.type for f in dc.fields(cls)}
    return cls(**{
        key: _from_dict(fieldtypes[key], value) if dc.is_dataclass(fieldtypes[key]) else value
        for key, value in data.items()
    })

def read_config(path_to_config_file: str = defaults.CONFIG_FILE_PATH) -> RippySettings:
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
    return RippySettings.model_validate(toml) 

def write_config(model: RippySettings, config_file_path: str = defaults.CONFIG_FILE_PATH):
    with open(config_file_path, "w") as f:
        f.write(tk.dumps(model.model_dump()))

# if __name__ == "__main__":
#     core = CoreSettings()
#     movies = MovieSettings() 
#     tv = TVSettings()
#     makemkv = MakeMKVSettings(movies=movies, tv_shows=tv)
#     rs = RippySettings(core=core, makemkv=makemkv)
#
#     print(tk.dumps(rs.model_dump()))
#     print(get_description(MovieSettings, "min_title_length"))
#
#     write_config(rs, "./temp-model.toml")
#     rs = read_config("./temp-model.toml")
#     print(rs)

import os
import uuid
import pytest
from typer.testing import CliRunner
from rippy.core.config import RippyConfig
from rippy.main import app
import logging
import tempfile
import shutil

import rippy.commands.config as cfg

logger = logging.getLogger(__name__)


@pytest.fixture
def my_temp_dir():
    """
    Simple fixure that creates a temp directory.
    """
    path = tempfile.mkdtemp()
    yield path  # setup phase
    shutil.rmtree(path)


@pytest.mark.cli
def test_config(my_temp_dir):
    runner = CliRunner()

    path_to_config_file = f"{my_temp_dir}/rippy.toml"
    api_key = str(uuid.uuid1())
    min_length_movie = str(123123)

    logger.info(f"Attmpting to save configuration to {path_to_config_file}")
    actual = runner.invoke(app, [
        "config",
        "set",
        "api-key",
        api_key,
        "--config-file", path_to_config_file])
    assert actual.exit_code == 0, f"Expected {actual.exit_code} to be 0!"

    actual = runner.invoke(app, [
        "config",
        "set",
        "rip-dir",
        my_temp_dir,
        "--config-file", path_to_config_file])
    assert actual.exit_code == 0, f"Expected {actual.exit_code} to be 0!"

    actual = runner.invoke(app, [
        "config",
        "set",
        "min-length-movie",
        min_length_movie,
        "--config-file", path_to_config_file])
    assert actual.exit_code == 0, f"Expected {actual.exit_code} to be 0!"

    cfg = RippyConfig.read(path_to_config_file=path_to_config_file)

    assert cfg.api_key == api_key, f"Expected cfg.api_key to be {api_key}!"
    assert cfg.rip_dir == my_temp_dir, f"Expected cfg.rip_dir to be {
        my_temp_dir}!"
    assert cfg.min_length_movie == min_length_movie, f"Expected cfg.min_length_movie to be {
        min_length_movie}!"

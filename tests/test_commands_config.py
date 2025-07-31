import pytest 
from typer.testing import CliRunner   
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
    actual = runner.invoke(app, ["config", "api_key", "1234abcd"])
    assert actual.exit_code == 0, f"Expected {actual.exit_code} to be 0!"


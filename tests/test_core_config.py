import logging
import os
import shutil
import tempfile
import uuid

import pytest

import rippy.core.config as cfg
import rippy.core.defaults as d

logger = logging.getLogger(__name__)


@pytest.fixture
def my_temp_dir():
    """
    Simple fixure that creates a temp directory.
    """
    path = tempfile.mkdtemp()
    yield path  # setup phase
    shutil.rmtree(path)


def test_write_config(my_temp_dir):
    """Tests the serialization and deserialization of config files."""

    # Default values
    defaults = d.get_defaults()

    # Create a config instance with default values
    expected = cfg.RippyConfig()

    # Create a file path to a location in /tmp
    path_to_config_file = os.path.join(my_temp_dir, defaults.CONFIG_FILE)

    # Write config to file as TOML
    logger.info(f"Writing config to `{path_to_config_file}` with defaults:")
    logger.debug(f"\t {expected}")
    cfg.write_config(expected, path_to_config_file=path_to_config_file, overwrite=True)

    # Read it back and make sure everything is the same
    actual = cfg.read_config(path_to_config_file=path_to_config_file)
    assert_are_equal(expected, actual)
    logger.info(f"OK: configuration file exists at `{path_to_config_file}`!")

    # Create a new config with custom values
    expected = cfg.RippyConfig()
    expected.core.api_key = str(uuid.uuid1())
    expected.makemkv.tv_show_min_title_length = 360

    # Write config to file as TOML
    logger.info(f"Writing config to `{path_to_config_file}` with custom values:")
    logger.debug(f"\t {expected}")
    cfg.write_config(expected, overwrite=True, path_to_config_file=path_to_config_file)

    # Read it back and make sure everything is the same
    actual = cfg.read_config(path_to_config_file)
    assert_are_equal(expected, actual)
    logger.info(f"OK: configuration file exists at `{path_to_config_file}`!")


def assert_are_equal(expected: cfg.RippyConfig, actual: cfg.RippyConfig):
    assert expected.core.api_key == actual.core.api_key
    assert expected.core.rip_dir == actual.core.rip_dir
    assert (
        expected.makemkv.movie_min_title_length == actual.makemkv.movie_min_title_length
    )
    assert (
        expected.makemkv.tv_show_min_title_length
        == actual.makemkv.tv_show_min_title_length
    )

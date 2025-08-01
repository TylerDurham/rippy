import logging
import os
import shutil
import tempfile
import uuid

import pytest

import rippy.core.config as cfg
import rippy.core.defaults as d

logger = logging.getLogger(__name__)

# Default values
defaults = d.get_defaults()


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

    # Create a config instance with default values
    expected = cfg.RippyConfig()

    # Create a file path to a location in /tmp
    path_to_config_file = os.path.join(my_temp_dir, defaults.CONFIG_FILE)

    # Write config to file as TOML
    logger.info(f"Writing config to `{path_to_config_file}` with defaults:")
    logger.debug(f"\t {expected}")
    expected.save(path_to_config_file=path_to_config_file, overwrite=True)

    # Read it back and make sure everything is the same
    actual = cfg.RippyConfig.read(path_to_config_file=path_to_config_file)
    assert_are_equal(expected, actual)
    logger.info(f"OK: configuration file exists at `{path_to_config_file}`!")

    # Create a new config with custom values
    expected = cfg.RippyConfig()
    expected.api_key = str(uuid.uuid1())
    expected.min_length_tv_episode = 360

    # Write config to file as TOML
    logger.info(f"Writing config to `{path_to_config_file}` with custom values:")
    logger.debug(f"\t {expected}")
    expected.save(overwrite=True, path_to_config_file=path_to_config_file)

    # Read it back and make sure everything is the same
    actual = cfg.RippyConfig.read(path_to_config_file)
    assert_are_equal(expected, actual)
    logger.info(f"OK: configuration file exists at `{path_to_config_file}`!")


def assert_are_equal(expected: cfg.RippyConfig, actual: cfg.RippyConfig):
    assert expected.api_key == actual.api_key
    assert expected.rip_dir == actual.rip_dir
    assert expected.min_length_movie == actual.min_length_movie
    assert expected.min_length_tv_episode == actual.min_length_tv_episode


def test_write_config_fail_no_overwrite(my_temp_dir):
    """Tests that write_file won't overrite an existing file UNLESS you specify overwrite = True."""

    # Create a file path to a location in /tmp
    path_to_config_file = os.path.join(my_temp_dir, defaults.CONFIG_FILE)

    # Write first to make sure the file exists in the temp directory
    cfg.RippyConfig().save(path_to_config_file=path_to_config_file)

    with pytest.raises(FileExistsError):
        cfg.RippyConfig().save(path_to_config_file=path_to_config_file)

    logger.info(
        f"OK: Not specifiying `overwrite` = True raised error of type `FileExistsError`!"
    )

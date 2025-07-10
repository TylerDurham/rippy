import pytest
import uuid 
import tempfile
from rippy.config import ensure_path, read_config, write_config, RippyConfig 
from rippy.defaults import get_defaults
import shutil
import os
import dataclasses as dc
import logging

logger = logging.getLogger(__name__)

DEFAULTS = get_defaults()

@dc.dataclass
class GoodInput():
    api_key: str
    rip_dir: str

@pytest.fixture
def api_key():
    return str(uuid.uuid1())

@pytest.fixture
def my_temp_dir():
    path = tempfile.mkdtemp()
    yield path  # setup phase
    shutil.rmtree(path)

def test_write_and_read(api_key, my_temp_dir):

    for _ in range(1, 5):
        config_file_path = os.path.join(my_temp_dir, DEFAULTS.CONFIG_FILE)
        
        # Create an instance...
        expected = RippyConfig()
        expected.core.api_key = api_key
        expected.core.rip_dir = os.path.join(my_temp_dir, DEFAULTS.APP_NAME)

        # ... write to disk
        logger.debug(expected)
        write_config(expected, True, path_to_config_file=config_file_path)

        # Read from disk...
        output = read_config(config_file_path)

        # ... make sure everything matches
        assert expected == output
        assert expected.core.api_key == output.core.api_key
        assert expected.core.rip_dir == output.core.rip_dir

def test_exists_no_overwrite(api_key, my_temp_dir):
    """
    Ensures that writing to a config that exists WITHOUT the overwrite parameter fails.
    """
    with pytest.raises(FileExistsError):
        for _ in range(1, 5):            
            config_file_path = os.path.join(my_temp_dir, DEFAULTS.CONFIG_FILE)

            logger.debug(config_file_path)
            expected = RippyConfig()
            expected.core.api_key = api_key
            expected.core.rip_dir = os.path.join(my_temp_dir, DEFAULTS.APP_NAME)
            logger.debug(expected)
            
            # Write once
            write_config(expected, True, path_to_config_file=config_file_path)

            # Try to write again WITHOUT specifying overwrite = True
            write_config(expected, False, path_to_config_file=config_file_path) # Write with overwrite = True or the file won't exist

def test_ensure_path(my_temp_dir):
    for _ in range(1, 5):
        new_path = os.path.join(my_temp_dir, DEFAULTS.APP_NAME, str(uuid.uuid1()))

        logger.debug(f"Calling ensure_path('{new_path}')")
        ensure_path(new_path)
        assert os.path.exists(new_path)


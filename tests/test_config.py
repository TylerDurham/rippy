import pytest
import uuid 
import tempfile
from rippy.core import config as cfg 
import shutil
import os
import dataclasses as dc
import logging

logger = logging.getLogger(__name__)

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
        config_file_path = os.path.join(my_temp_dir, cfg.CONFIG_FILE)
        
        # Create an instance...
        expected = cfg.RippyConfig()
        expected.core.api_key = api_key
        expected.core.rip_dir = os.path.join(my_temp_dir, cfg.APP_NAME)

        # ... write to disk
        logger.debug(expected)
        cfg.write_file(expected, True, config_file_path)

        # Read from disk...
        output = cfg.read_file(config_file_path)

        # ... make sure everything matches
        assert expected == output
        assert expected.core == output.core
        assert expected.core.api_key == output.core.api_key
        assert expected.core.rip_dir == output.core.rip_dir

def test_exists_no_overwrite(api_key, my_temp_dir):
    """
    Ensures that writing to a config that exists WITHOUT the overwrite parameter fails.
    """
    with pytest.raises(FileExistsError):
        for _ in range(1, 5):            
            config_file_path = os.path.join(my_temp_dir, my_temp_dir)

            logger.debug(config_file_path)
            expected = cfg.RippyConfig()
            expected.core.api_key = api_key
            expected.core.rip_dir = os.path.join(my_temp_dir, cfg.APP_NAME)
            logger.debug(expected)

            cfg.write_file(expected, True) # Write with overwrite = True or the file won't exist
            cfg.write_file(expected)
            
def test_ensure_path(my_temp_dir):
    for _ in range(1, 5):
        new_path = os.path.join(my_temp_dir, cfg.APP_NAME, str(uuid.uuid1()))

        logger.debug(f"Calling ensure_path('{new_path}')")
        cfg.ensure_path(new_path)
        assert os.path.exists(new_path)
            

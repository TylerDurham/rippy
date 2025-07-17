from re import DEBUG
import pytest
import logging
from rippy.commands.init import init

logger = logging.getLogger(__name__)

def test_movie_arg_errors():
    with pytest.raises(ValueError):
        init("movie", "Fear", read=True) # No need to pass in title when -r is specified.
    
    logger.debug(f"OK! rippy init 'Fear' -r raised ValueError")

    with pytest.raises(ValueError):
        init(search=True) # Cannot search without a title or -r flag

    logger.debug(f"OK! rippy init -s raised ValueError")



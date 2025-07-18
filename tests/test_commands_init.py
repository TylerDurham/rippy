import logging
from re import DEBUG

from typing import List

import pytest

from rippy.commands.init import app as cmd_init

from typer.testing import CliRunner

logger = logging.getLogger(__name__)

@pytest.mark.cli
def test_movie():

    runner = CliRunner()
    actual = runner.invoke(cmd_init, ["movie", "Fear", "--search"])
    assert actual.exit_code == 0, f"Expected {actual.exit_code} to be 0!"


    # init("movie", "Fear", search=True)
    # init("movie", read=True)

@pytest.mark.cli
def test_movie_arg_errors():

    runner = CliRunner()

    inputs = ["movie", "Fear", "--read"]
    assert_movie_arg_error(cmd_init, inputs)
    
    # logger.debug(f"OK! rippy init 'Fear' -r raised ValueError")
    #
    # with pytest.raises(ValueError):
    #     init(search=True)  # Cannot search without a title or -r flag
    #
    # logger.debug(f"OK! rippy init (no args) raised ValueError")
    #
    # with pytest.raises(ValueError):
    #     init()  # no inputs
    #
    # logger.debug(f"OK! rippy init -s raised ValueError")
    #
    # with pytest.raises(ValueError):
    #     init("foo", "Fear", search=True)

def assert_movie_arg_error(app, inputs: List[str]):
    
    runner = CliRunner()
    result = runner.invoke(app, inputs)
    assert result.exit_code == 1
    logger.debug(result) 


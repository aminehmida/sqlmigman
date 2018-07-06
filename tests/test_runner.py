"""Test sqlmigman runner"""
import pytest

from sqlmigman import runner

TEST_SUCCESS_CMD = 'echo "Test OK"'
TEST_SUCCESS_CMD_OUTPUT = 'Test OK\n'
TEST_FAIL_CMD = 'ls /the_void_path'
TEST_FAIL_CMD_OUTPUT = 'No such file or directory'


def test_run_in_shell_sucess():
        assert runner.run_in_shell(TEST_SUCCESS_CMD) == TEST_SUCCESS_CMD_OUTPUT


# TODO: Find more pythonic way to test this (with unittest?)
def test_run_in_shell_fail():
    with pytest.raises(runner.ExecError) as e:
        runner.run_in_shell(TEST_FAIL_CMD)
    assert TEST_FAIL_CMD_OUTPUT in str(e)

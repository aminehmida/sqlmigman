"""Test sqlmigman transform."""
import mock
import pytest

from sqlmigman import transform

TEST_CMD_TEMPLATE = ('==$(-u %bla%)==$(-u %bla% is cool)==%bla%'
                     '==$(-p %password%)==$(-x %unused%)==%unused%==')

TEST_CMD_TRANSFORMED = '==-u 1==-u 1 is cool==1==-p p@ssW0rd======'

TEST_CMD_VALS = [{'bla': '1'},
                 {'password': 'p@ssW0rd'}]


def test_transform():
    assert (transform(TEST_CMD_TEMPLATE, *TEST_CMD_VALS) ==
            TEST_CMD_TRANSFORMED)

"""Test sqlmigman core."""
import logging
import mock
import pytest

import sqlmigman.core as core


@pytest.fixture
def smm(mocker):
    mig_scripts_dir = '/test'
    mig_scripts_regexp = '(\d+)\D*\.sql'
    sql_host = 'localhost'
    sql_user = 'root'
    sql_password = 'p@ssw0rd'
    sql_db_name = 'testdb'
    mig_apply_cmd = ('mysql $(-u %user%) $(-p %password%) '
                     '$(-h %host%) $( %db%) < %script%')
    mig_get_version_cmd = 'echo -n 123'
    mig_update_version_cmd = ('mysql $(-u %user%) $(-p %password%) '
                              '$(-h %host%) -e "UPDATE version '
                              'SET version=%version%;"')
    return core.SqlMigMan(mig_scripts_dir,
                          mig_scripts_regexp,
                          sql_host,
                          sql_user,
                          sql_password,
                          sql_db_name,
                          mig_apply_cmd,
                          mig_get_version_cmd,
                          mig_update_version_cmd)


@mock.patch('os.listdir', return_value=['1-mocked.sql'])
def test_matching_scripts_sorted(mocker, smm):
    assert (smm.matching_scripts_sorted() ==
            [{'version': 1, 'path': '/test/1-mocked.sql'}])


def test_current_schema_version(smm):
    assert smm.current_schema_version() == 123

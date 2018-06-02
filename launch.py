#!/usr/bin/env python2.7
import logging
import argparse
import configparser
import sys
import os

from sqlmigman.core import SqlMigMan
from sqlmigman.runner import ExecError

CONFIG_FILE = 'sqlmigman.cfg'
CONFIG_LOCATIONS = ['/etc',
                    '/usr/local/etc',
                    os.curdir]

parser = argparse.ArgumentParser(description='Database schema '
                                             'upgrade manager.')

parser.add_argument('--mig-dir',
                    '-d',
                    help='Directory where .sql file are located')
parser.add_argument('--sql-host',
                    '-s',
                    help='Sql server host or ip address.')
parser.add_argument('--sql-user',
                    '-u',
                    help='Database user name.')
parser.add_argument('--sql-password',
                    '-p',
                    help='Database user password.')
parser.add_argument('--sql-db',
                    '-n',
                    help='Database name')
parser.add_argument('--continue-on-fail',
                    '-f',
                    default=False,
                    help='Continue upgrade when '
                         'intermediary failure is detected.')
parser.add_argument('--mig-cmd',
                    '-c',
                    help='Migration command template')
parser.add_argument('--mig-regexp',
                    '-r',
                    default='(\d+)\D*\.sql',
                    help='Regular expression used to match and '
                         'extract schema version '
                         'from .sql upgrade script. '
                         'Default will match <version><name>.sql')
parser.add_argument('--mig-update-cmd',
                    '-t',
                    help='This command will be run when all update script are '
                         'applied with success. Use a syntax simular to '
                         '--arg-cmd with addition of %%version%% variable'
                         'that contains version of the latest script applied')
parser.add_argument('--mig-version-cmd',
                    '-v',
                    help='This command will be run to extract current '
                         'database schema version. Same syntax as --mig-cmd')

args = parser.parse_args()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    cfg = configparser.RawConfigParser()
    cfg.read([os.path.join(conf_path, CONFIG_FILE)
              for conf_path in CONFIG_LOCATIONS])

    # TODO: Find more pythonic way to fall back to config file for defaults
    mig_dir = args.mig_dir
    if mig_dir is None and cfg.has_option('migration', 'scripts_dir'):
        mig_dir = cfg.get('migration', 'scripts_dir')
    mig_regexp = args.mig_regexp
    if mig_regexp is None and cfg.has_option('migration', 'script_regexp'):
        mig_regexp = cfg.get('migration', 'script_regexp')
    sql_host = args.sql_host
    if sql_host is None and cfg.has_option('sql', 'host'):
        sql_host = cfg.get('sql', 'host')
    sql_user = args.sql_user
    if sql_user is None and cfg.has_option('sql', 'user'):
        sql_user = cfg.get('sql', 'user')
    sql_password = args.sql_password
    if sql_password is None and cfg.has_option('sql', 'password'):
        sql_password = cfg.get('sql', 'password')
    sql_db = args.sql_db
    if sql_db is None and cfg.has_option('sql', 'db'):
        sql_db = cfg.get('sql', 'db')
    mig_cmd = args.mig_cmd
    if mig_cmd is None and cfg.has_option('migration', 'apply_cmd'):
        mig_cmd = cfg.get('migration', 'apply_cmd')
    mig_version_cmd = args.mig_version_cmd
    if mig_version_cmd is None and cfg.has_option('migration', 'version_cmd'):
        mig_version_cmd = cfg.get('migration', 'version_cmd')
    mig_update_cmd = args.mig_update_cmd
    if mig_update_cmd is None and cfg.has_option('migration',
                                                 'version_update_cmd'):
        mig_update_cmd = cfg.get('migration', 'version_update_cmd')

    # Check mandatory args
    if mig_dir is None:
        logging.error("No migration directory provided."
                      " Use config file or --mig-dir argument")
        sys.exit()

    sqlmigman = SqlMigMan(mig_dir,
                          mig_regexp,
                          sql_host,
                          sql_user,
                          sql_password,
                          sql_db,
                          mig_cmd,
                          mig_version_cmd,
                          mig_update_cmd)

    logging.info("Staring database migration")

    # Extract upgrade file list that match --mig-regexp
    sql_scripts = sqlmigman.matching_scripts_sorted()
    if len(sql_scripts) == 0:
        logging.info("No matching sql file found. Noting to apply.")
        sys.exit()

    # Extracting existing database version
    try:
        current_db_version = sqlmigman.current_schema_version()
    except ExecError, e:
        logging.critical("Can not detect current "
                         "database schema version: %s" % str(e))

    # Apply migration scripts
    for script in sql_scripts:
        if script['version'] > current_db_version:
            try:
                stdout = sqlmigman.apply_script(script['path'])
                logging.info("%s applied with success" % script['path'])
                logging.debug("stdout for appling %s: %s" %
                              (script['path'], stdout))
            except ExecError, e:
                logging.error("Failed to apply %s "
                              "with error: %s" % (script['path'], str(e)))
                if not args.continue_on_fail:
                    logging.info("Migration terminated because of an error "
                                 "when applying script: %s" % script['path'])
                    sys.exit()
            else:
                try:
                    sqlmigman.update_schema_version(script['version'])
                except ExecError, e:
                    logging.critical("Can not update "
                                     "database schema version: %s" % str(e))


if __name__ == "__main__":
    main()

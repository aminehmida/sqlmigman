# SQL (Mig)ration (Man)ager [![Build Status](https://travis-ci.com/aminehmida/sqlmigman.svg?branch=master)](https://travis-ci.com/aminehmida/sqlmigman)

Highly extensible tool to manage SQL database schema migration. Can support MySql/Postgrasql ...

**Note:** This is still an alpha version. Expect dragons!

## Installing

Start by cloning this project. No external dependency was used. Tested and working in python 2.7 and 3.6

## Getting Started

SqlMigMan is used to manage database schema updates. It is highly extensible because it uses a template syntax to do the following:

1. Match update scripts file name with a regexp. You can use `(\d+)\D*\.sql` to match `<version><name>.sql` and `<version>-<name>.sql` at the same time for example. Vesion is matched with `()`
2. Extract existing database schema version
3. Apply update scripts higher then current schema with order (from low to high)
4. Update the schema version after each successful update

Check provided config example `sqlmigman.cfg.example` and customise for your needs then copy config to same working dir, `/etc/` or `/usr/local/etc/`. Finally, launch with `python launch.py`

### Example of config file to manage MySQL database updates:

```
scripts_dir = /path/to/update/scripts
script_regexp = (\d+)\D*\.sql
apply_cmd = mysql $(-u %user% )$(-p %password% )$(-h %host% )%db% < %script%
version_cmd = mysql $(-u %user% )$(-p %password% )$(-h %host% )%db% -e "SELECT version FROM version"
version_update_cmd = mysql $(-u %user% )$(-p %password% )$(-h %host% )%db% -e "UPDATE version SET version=%version%"
```

**Note:** All configs can be passed using command line. Type `python launch.py -h` to find matching arguments names:

```
usage: launch.py [-h] [--mig-dir MIG_DIR] [--sql-host SQL_HOST]
                 [--sql-user SQL_USER] [--sql-password SQL_PASSWORD]
                 [--sql-db SQL_DB] [--continue-on-fail CONTINUE_ON_FAIL]
                 [--mig-cmd MIG_CMD] [--mig-regexp MIG_REGEXP]
                 [--mig-update-cmd MIG_UPDATE_CMD]
                 [--mig-version-cmd MIG_VERSION_CMD]

Database schema upgrade manager.

optional arguments:
  -h, --help            show this help message and exit
  --mig-dir MIG_DIR, -d MIG_DIR
                        Directory where .sql file are located
  --sql-host SQL_HOST, -s SQL_HOST
                        Sql server host or ip address.
  --sql-user SQL_USER, -u SQL_USER
                        Database user name.
  --sql-password SQL_PASSWORD, -p SQL_PASSWORD
                        Database user password.
  --sql-db SQL_DB, -n SQL_DB
                        Database name
  --continue-on-fail CONTINUE_ON_FAIL, -f CONTINUE_ON_FAIL
                        Continue upgrade when intermediary failure is
                        detected.
  --mig-cmd MIG_CMD, -c MIG_CMD
                        Migration command template
  --mig-regexp MIG_REGEXP, -r MIG_REGEXP
                        Regular expression used to match and extract schema
                        version from .sql upgrade script. Default will match
                        <version><name>.sql
  --mig-update-cmd MIG_UPDATE_CMD, -t MIG_UPDATE_CMD
                        This command will be run when all update script are
                        applied with success. Use a syntax simular to --arg-
                        cmd with addition of %version% variablethat contains
                        version of the latest script applied
  --mig-version-cmd MIG_VERSION_CMD, -v MIG_VERSION_CMD
                        This command will be run to extract current database
                        schema version. Same syntax as --mig-cmd
```

### Command templates:
You can use two types of command template formats:

- Simple format `%var_name%`: This will be simply replaced with `var_name` if defined. If `var_name` is not defined `%var_name%` will be removed from the template.

- Composite format `$(cont1 %var_name% const2)`: with this format`$(` and `)` will be removed, `%var_name%` will be replaced with its value and `const1`/`const2` are kept as is.

## Running tests

Start by installing `requirements_dev.txt` and run `pycodestyle --show-pep8 *.py ./sqlmigman/*.py ./tests/*.py; pytest -vv --showlocals ./tests` to execute style check and unit tests.

## TODO:
- Add support for environment variables.
- Add `--dry-run`
- Build docker container
- Add `--config` flag
- Automate style and unit tests
- Add more unit tests
- Add integration tests with docker

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

# SQL (Mig)ration (Man)ager

Highly extensible tool to manage SQL database schema migration. Can support MySql/Postgrasql ...

## Installing

Start by cloning this project. No external dependency was used and tested only with python 2.7.

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

**Note:** All configs can be passed using command line. Type `python launch.py -h` to find matching arguments names.

### Command templates:
You can use two types of command template formats:

- Simple format `%var_name%`: This will be simply replaced with `var_name` if defined. If `var_name` is not defined `%var_name%` will be removed from the template.

- Composite format `$(cont1 %var_name% const2)`: with this format`$(` and `)` will be removed, `%var_name%` will be replaced with its value and `const1`/`const2` are kept as is.

## Running tests

Start by installing `requirements_dev.txt` and run `pycodestyle --show-pep8 *.py ./sqlmigman/*.py ./tests/*.py; pytest -vv --showlocals ./tests` to execute style check and unit tests.

## TODO:
- Add support for environment variables.
- Add `--dry-run`
- Check if this will work with python3
- Build docker container
- Add `--config` flag
- Automate style and unit tests
- Add more unit tests
- Add integration tests with docker

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

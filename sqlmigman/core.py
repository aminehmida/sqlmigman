"""sqlmigman main lib"""
import os
import re

from sqlmigman import run_in_shell, ExecError, transform


class SqlMigMan:
    """SqlMigMan main class"""
    def __init__(self,
                 mig_scripts_dir,
                 mig_scripts_regexp,
                 sql_host,
                 sql_user,
                 sql_password,
                 sql_db_name,
                 mig_apply_cmd,
                 mig_get_version_cmd,
                 mig_update_version_cmd):
        """Constructor of SqlMigMan"""

        self.mig_scripts_dir = mig_scripts_dir
        self.mig_scripts_regexp = mig_scripts_regexp
        self.sql_host = sql_host
        self.sql_user = sql_user
        self.sql_password = sql_password
        self.sql_db_name = sql_db_name
        self.mig_apply_cmd = mig_apply_cmd
        self.mig_get_version_cmd = mig_get_version_cmd
        self.mig_update_version_cmd = mig_update_version_cmd

    def current_schema_version(self):
        """Return current database schema version"""
        return int(run_in_shell(
                    transform(self.mig_get_version_cmd,
                              {'host': self.sql_host},
                              {'user': self.sql_user},
                              {'password': self.sql_password},
                              {'db': self.sql_db_name})))

    def update_schema_version(self, version):
        """update database schema version"""
        return run_in_shell(
                  transform(self.mig_get_version_cmd,
                            {'host': self.sql_host},
                            {'user': self.sql_user},
                            {'password': self.sql_password},
                            {'db': self.sql_db_name},
                            {'version': version}))

    def matching_scripts_sorted(self):
        """Return a script_list of {path, version} of all matching
        migration scripts sorted by version (low to high)"""

        script_list = []
        for f in os.listdir(self.mig_scripts_dir):
            m = re.match(self.mig_scripts_regexp, f)
            if m:
                version = int(m.group(1))
                index = 0
                while (len(script_list) > 0 and
                        index <= len(script_list)-1 and
                        script_list[index]['version'] < version):
                    index += 1
                script_list.insert(index,
                                   {'version': version,
                                    'path': os.path.join(self.mig_scripts_dir,
                                                         f)})
        return script_list

    def apply_script(self, path):
        """Apply one migration script"""
        return run_in_shell(
                  transform(self.mig_get_version_cmd,
                            {'host': self.sql_host},
                            {'user': self.sql_user},
                            {'password': self.sql_password},
                            {'db': self.sql_db_name},
                            {'script': path}))

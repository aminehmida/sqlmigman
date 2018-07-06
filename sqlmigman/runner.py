"""sqlmigman shell command executer"""
import subprocess as sp


class ExecError(Exception):
    pass


def run_in_shell(cmd):
    proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise ExecError(err.decode('utf-8'))

    return out.decode('utf-8')

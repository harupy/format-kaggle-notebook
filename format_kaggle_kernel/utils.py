import os
import subprocess
import sys

import jupytext


def run_shell(command):
    p = subprocess.Popen(
        [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = p.communicate()

    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")  # stderr contains warnings.

    if p.returncode != os.EX_OK:
        print(stdout)
        print(stderr)
        raise sys.exit(p.returncode)

    if stdout != "":
        print(stdout)

    if stderr != "":
        print(stderr)

    return p.returncode


def is_script(path):
    return path.endswith(".py")


def is_notebook(path):
    return path.endswith(".ipynb")


def is_kernel(path):
    return is_script(path) or is_notebook(path)


def find_kernel(d):
    name = [f for f in os.listdir(d) if is_kernel(f)][0]
    return os.path.join(d, name)


def replace_ext(path, ext):
    if not ext.startswith("."):
        ext = "." + ext
    return os.path.splitext(path)[0] + ext


def nb_to_py(nb_path, py_path):
    jupytext.write(jupytext.read(nb_path), py_path, fmt=".py")


def py_to_nb(py_path, nb_path):
    jupytext.write(jupytext.read(py_path), nb_path, fmt=".ipynb")

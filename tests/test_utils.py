import json
import os

import pytest


from format_kaggle_kernel import utils


def read_json(path):
    with open(path) as f:
        return json.load(f)


def remove_comments_and_blank_lines(text):
    return "\n".join(
        [l for l in text.split("\n") if l.strip() != "" and not l.startswith("#")]
    )


def test_run_shell(capsys):
    utils.run_shell("echo hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n\n"
    assert captured.err == ""


def test_run_shell_exit_on_error():
    with pytest.raises(SystemExit):
        utils.run_shell("find")


def test_is_script():
    assert utils.is_script("test.py")
    assert not utils.is_script("test.ipynb")


def test_is_notebook():
    assert utils.is_notebook("test.ipynb")
    assert not utils.is_notebook("test.py")


def test_is_kernel():
    assert utils.is_kernel("test.py")
    assert utils.is_kernel("test.ipynb")
    assert not utils.is_kernel("test.md")


@pytest.mark.parametrize("ext", [".py", ".ipynb"])
def test_find_kernel(tmpdir, ext):
    tmpdir = str(tmpdir)
    path = os.path.join(tmpdir, "test" + ext)
    with open(path, "w") as f:
        f.write("")

    assert utils.find_kernel(tmpdir) == path


def test_replace_ext():
    assert utils.replace_ext("test.py", ".ipynb") == "test.ipynb"
    assert utils.replace_ext("test.py", "ipynb") == "test.ipynb"


def test_py_to_nb(tmpdir):
    py_path = os.path.join(tmpdir, "test.py")
    nb_path = os.path.join(tmpdir, "test.ipynb")

    py_src = 'print("hello world")'
    with open(py_path, "w") as f:
        f.write(py_src)

    utils.py_to_nb(py_path, nb_path)

    assert os.path.exists(nb_path)
    assert read_json(nb_path)["cells"][0]["source"][0] == py_src


def test_nb_to_py(tmpdir):
    nb_src = r"""
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"hello world\")"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": 3
  },
  "orig_nbformat": 2
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
""".strip()

    nb_path = os.path.join(tmpdir, "test.ipynb")
    py_path = os.path.join(tmpdir, "test.py")

    with open(nb_path, "w") as f:
        f.write(nb_src)

    utils.nb_to_py(nb_path, py_path)
    # jupytext adds header lines to the generated script.
    py_src = remove_comments_and_blank_lines(open(py_path).read())

    assert os.path.exists(py_path)
    assert py_src == json.loads(nb_src)["cells"][0]["source"][0]

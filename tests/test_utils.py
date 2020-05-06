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
        utils.run_shell("unknown")


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
    p = tmpdir.join("test" + ext)
    p.write("")
    assert utils.find_kernel(tmpdir.strpath) == p.strpath


@pytest.mark.parametrize("ext", [".ipynb", "ipynb"])
def test_replace_ext(ext):
    assert utils.replace_ext("test.py", ext) == "test.ipynb"


def test_py_to_nb(tmpdir):
    py = tmpdir.join("test.py")
    nb = tmpdir.join("test.ipynb")

    py_src = 'print("hello world")'
    py.write(py_src)
    utils.py_to_nb(py.strpath, nb.strpath)

    assert os.path.exists(nb.strpath)
    assert read_json(nb.strpath)["cells"][0]["source"][0] == py_src


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

    nb = tmpdir.join("test.ipynb")
    py = tmpdir.join("test.py")
    nb.write(nb_src)

    utils.nb_to_py(nb.strpath, py.strpath)
    # jupytext adds header lines to the generated script.
    py_src = remove_comments_and_blank_lines(py.read())

    assert os.path.exists(py.strpath)
    assert py_src == json.loads(nb_src)["cells"][0]["source"][0]


def test_format_source(tmpdir):
    source = """
hello
world
""".strip()

    source_formatted = """
# hello
# world
""".strip()

    p = tmpdir.join("test.txt")
    p.write(source)
    utils.format_source(p, lambda source: [f"# {l}" for l in source])
    assert "".join(p.readlines()) == source_formatted


def test_comment_magic(tmpdir):
    source = """
# %% [code]
%%time

# %% [code]
!ls
""".strip()

    source_formatted = """
# %% [code]
# %%time

# %% [code]
# !ls
""".strip()

    p = tmpdir.join("test.py")
    p.write(source)
    utils.comment_magic(p)
    assert p.read() == source_formatted


def test_uncomment_magic(tmpdir):
    source = """
# %% [code]
# %%time

# %% [code]
# !ls
""".strip()

    source_formatted = """
# %% [code]
%%time

# %% [code]
!ls
""".strip()

    p = tmpdir.join("test.py")
    p.write(source)
    utils.uncomment_magic(p)
    assert p.read() == source_formatted

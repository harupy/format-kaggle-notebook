import argparse
import os
import subprocess
import sys
import tempfile

import jupytext


def parse_args():
    parser = argparse.ArgumentParser(description="Format kernel")
    parser.add_argument(
        "-k",
        "--kernel",
        required=True,
        help="Kernel URL suffix in format <owner>/<kernel-name>",
    )

    return parser.parse_known_args()  # Use unknown arguments as black arguments.


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


def main():
    args, black_args = parse_args()  # `black_args` is a list of strings.
    kernel = args.kernel
    black_args = " ".join(black_args)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Fetch metadata too to push the kernel back to Kaggle after formatting.
        run_shell(f"kaggle kernels pull -m -p {tmpdir} {kernel}")

        kernel_path = find_kernel(tmpdir)

        if is_script(kernel_path):
            run_shell(f"black {black_args} {kernel_path}")

        elif is_notebook(kernel_path):
            # If notebook, do the following steps.
            # 1. Convert the notebook to a script.
            # 2. Format the script.
            #    (black raises an error if shell (!) or magic (%%) commands exist.)
            # 3 Convet the formatted script to a notebook.
            with tempfile.NamedTemporaryFile(suffix=".py") as tmp_path:
                tmp_path = tmp_path.name
                notebook = jupytext.read(kernel_path)
                jupytext.write(notebook, tmp_path, fmt=".py")
                run_shell(f"black {black_args} {tmp_path}")
                script = jupytext.read(tmp_path)
                jupytext.write(script, kernel_path)

        else:
            ext = os.path.splitext(kernel_path)[-1]
            raise ValueError("Invalid file type: '{}'".format(ext))

        run_shell(f"kaggle kernels push -p {tmpdir}")
        run_shell(f"kaggle kernels status {kernel}")  # should return "queued".


if __name__ == "__main__":
    main()

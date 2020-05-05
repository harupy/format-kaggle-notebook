import argparse
import os
import tempfile

from format_kaggle_kernel import utils


def parse_args():
    parser = argparse.ArgumentParser(description="Format kernel")
    parser.add_argument(
        "-k",
        "--kernel",
        required=True,
        help="Kernel URL suffix in format <owner>/<kernel-name>",
    )
    return parser.parse_known_args()  # Use unknown arguments as black arguments.


def main():
    args, black_args = parse_args()  # `black_args` is a list of strings.
    kernel = args.kernel
    black_args = " ".join(black_args)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Fetch metadata too to push the kernel back to Kaggle after formatting.
        utils.run_shell(f"kaggle kernels pull -m -p {tmpdir} {kernel}")

        kernel_path = utils.find_kernel(tmpdir)

        if utils.is_script(kernel_path):
            utils.run_shell(f"black {black_args} {kernel_path}")

        elif utils.is_notebook(kernel_path):
            # If notebook, do the following steps.
            # 1. Convert the notebook to a script.
            # 2. Format the script.
            #    (black raises an error if shell (!) or magic (%%) commands exist.)
            # 3 Convet the formatted script to a notebook.
            with tempfile.NamedTemporaryFile(suffix=".py") as py_path:
                py_path = py_path.name
                utils.nb_to_py(kernel_path, py_path)
                utils.run_shell(f"black {black_args} {py_path}")
                utils.py_to_nb(py_path, kernel_path)

        else:
            ext = os.path.splitext(kernel_path)[-1]
            raise ValueError("Invalid file type: '{}'".format(ext))

        utils.run_shell(f"kaggle kernels push -p {tmpdir}")
        utils.run_shell(f"kaggle kernels status {kernel}")  # should return "queued".


if __name__ == "__main__":
    main()

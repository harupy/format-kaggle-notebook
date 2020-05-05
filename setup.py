import os
from setuptools import find_packages, setup


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


# Use README.md as a long description.
def get_long_description() -> str:
    with open(os.path.join(ROOT_DIR, "README.md"), encoding="utf-8") as f:
        return f.read()


def get_install_requires():
    with open(os.path.join(ROOT_DIR, "requirements.txt"), encoding="utf-8") as f:
        return [
            l.strip()
            for l in f.readlines()
            # Ignore comments and blank lines
            if not (l.startswith("#") or (l.strip() == ""))
        ]


setup(
    install_requires=get_install_requires(), packages=find_packages(),
)

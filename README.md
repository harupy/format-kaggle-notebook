# Format Kaggle Kernel

[![CI](https://github.com/harupy/format-kaggle-kernel/workflows/CI/badge.svg)](https://github.com/harupy/format-kaggle-kernel/actions?query=workflow%3ACI)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Format your Kaggle kernel with black from a command line.

## Installation

```bash
pip install git+https://github.com/harupy/foramt-kaggle-kernel
```

## Requirements

In order to use `format-kaggle-kernel`, you must first authenticate using an API token.

See: https://www.kaggle.com/docs/api

## How to run

```bash
format-kernel -k <user>/<kernel-slug>

# You can pass black options
format-kernel -k <user>/<kernel-slug> --line-length 100
```

## Limitation

`black` raises a syntax error when your kernel contains shell commands (e.g. `!ls`) or magic commands (e.g. `%time`).

# Contributing to Format Kaggle Kernel

## Table of Contents

1. [Create a development environment](#create-a-development-environment)
1. [Enable CLI](#enable-cli)
1. [Lint](#lint)
1. [Test](#test)

## Create a development environment

```bash
conda create -n <env_name> python=3.7
conda activate <env_name>

pip install -r requirements.txt -r requirements-dev.txt
```

## Enable CLI

```bash
pip install -e .
```

## Lint

```bash
flake8 .
black --check .
```

## Test

```bash
pytest tests
```

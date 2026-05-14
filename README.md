# Icedantic
A package that integrates with your Pydantic models and enables you to export Apache Iceberg table schemas.

## Installing

You can install directly from PyPI using e.g.

```bash
uv add icedantic
```

or

```bash
pip install icedantic
```

or you can install locally from file using:

```bash
uv pip install -e <location_on_disk>
```

## Developing

This repo provides a devcontainer to easily develop the package. It assumes you have `uv` and `fish` installed on your host system. This cannot be made optional because these assumptions involve bind mounts.

Install the package locally (symlinked) within the `venv` created by `uv` using:

```bash
uv pip install -e .
```

### Pre-commit

We use `pre-commit` to run a few hooks to ensure code quality and stuff like that. Please use the devcontainer, all this is taken care for you if you do so.

### Running tests

We use `tox` for bothing running the tests as well as running `pre-commit`. Please run `tox` to run your tests.

## Contributing

Please see `CONTRIBUTING.md`.

## Issues

If you discover bugs or other issues, please create an issue with a stack trace and code to reproduce. We have no predefined format for issues, just make sure there is enough info to reproduce.

## Why?

AFAIK there is nothing "ready to go" that offers the same functionality, bar doing the mapping yourself. Because I needed to do this in a neat way, might as well open source it.

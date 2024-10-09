# Contributing to release-feed-mediola

## Setting up release-feed-mediola for development

To set up release-feed-mediola, you need three things:

1. The Python version manager `pyenv`.

2. A system-wide Python installation.

3. The Python dependency manager `poetry`.

### Installing pyenv

The Python version manager `pyenv` makes sure you can always keep
the exact Python version required by release-feed-mediola,
regardless of your system Python.

#### Installing pyenv on Windows

While `pyenv` doesn’t support Windows, you can use a drop-in
replacement called `pyenv-win`.

To install `pyenv-win` on Windows, go to
[github.com/pyenv-win/pyenv-win](https://github.com/pyenv-win/pyenv-win#installation)
and follow one of the installation methods.

#### Installing pyenv on Linux

To install `pyenv` on Linux or WSL2, first make sure Python 3 is
installed. Then follow the _Basic GitHub Checkout_ method described
at [github.com/pyenv/pyenv](https://github.com/pyenv/pyenv#basic-github-checkout).

#### Installing pyenv on macOS

To install `pyenv` on macOS, run:

```shell
brew install pyenv
```

#### Checking your system-wide pyenv installation

To verify your `pyenv` is working, run:

```shell
pyenv --version
```

### Checking your system-wide Python installation

Make sure you have Python 3.8 or higher installed on your system
and available in your PATH.

To check, run:

```shell
python --version
```

If that fails, try:

```shell
python3 --version
```

Proceed after you’ve confirmed one of those to work.

### Installing Poetry

You’ll need `poetry` to manage development dependencies and the venv.

To install Poetry on Windows, use one of the
[installation methods](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
described in Poetry’s documentation.

To install Poetry on macOS, run:

```shell
brew install poetry
```

If you’re on Linux or WSL2, use your system package manager to
install Poetry.

Alternatively, use one of the
[installation methods](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
described in Poetry’s documentation.

#### Checking your Poetry installation

To verify Poetry is working, run:

```shell
poetry --version
```

### Setting up your virtual environment

To set up your virtual environment, follow these steps:

1. Go to the project root directory.

2. Run `pyenv install -s`.

3. Run `pyenv exec python -m venv .venv`.

4. Run `poetry install`.

You need to do the above steps only once.

To update your dependencies after a `git pull`, run `poetry update`.

## Development scripts and tasks

To see a list of available tasks, run: `poetry run poe tasks`

### Running release-feed-mediola

To execute release-feed-mediola, run:

```shell
poetry run poe feed [product_name]
```

For example, `poetry run poe feed neo` will generate a feed for
AIO CREATOR NEO.

For a list of valid product names, run `poetry run poe doc`, then
point your browser to
[release_feed_mediola.html#release_feed](http://localhost:8080/release_feed_mediola.html#release_feed).

### Running the tests

To execute the tests, run:

```shell
poetry run poe tests
```

To execute a single test, run e. g.:

```shell
poetry run poe tests -vv tests/test_api.py::test_from_dict
```

### Running the linter

To execute the linter, run:

```shell
poetry run poe linter
```

### Running the static type check

To execute the static type check, run:

```shell
poetry run poe typecheck
```

### Running the entire CI pipeline locally

If you have [act](https://github.com/nektos/act) installed and a
Docker daemon active, run:

```shell
act
```

If that command fails with an error message like:

> OCI runtime exec failed: exec failed: unable to start container process: exec: "node": executable file not found in $PATH: unknown

then run: `docker volume rm -f act-toolcache`

### Generating project documentation

To generate project documentation, run:

```shell
poetry run poe doc
```

To open the generated documentation with `man`, run:

```shell
poetry run poe man
```

## Maintenance

### Refreshing dependencies

If you get errors after a Git pull, refresh your dependencies:

```shell
poetry update
```

### Rebuilding the virtual environment

If you’ve run `poetry update` and you still get errors, rebuild
the virtual environment:

```shell
poetry install
```

### Checking release-feed-mediola’s dependencies for compatible updates

To check release-feed-mediola’s dependencies for compatible updates, run:

```shell
poetry update --dry-run
```

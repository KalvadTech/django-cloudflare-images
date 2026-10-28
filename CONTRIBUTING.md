# Contributing

Contributions are welcome. To contribute to django-cloudflare-images:

## Development setup

Python 3.10 or later is required.

1. Fork and clone the repository.
2. Install the development environment:

```sh
make install
```

This creates an `env/` virtual environment and installs the development
dependencies.

## Make targets

| Command | Description |
| --- | --- |
| `make install` | Create `env/` and install development dependencies. |
| `make clean` | Remove `env/`, `.tox/`, build artifacts, and egg info. |
| `make format` | Format the code with Ruff. |
| `make check` | Run Ruff lint checks. |
| `make static-check` | Run the `ty` type checker. |
| `make test` | Run the test suite with tox. |
| `make package` | Build the sdist and wheel in `dist/`. |

## Before submitting

- Add or update tests for your changes.
- Run `make format`.
- Run `make check`.
- Run `make static-check`.
- Run `make test`.
- Open a pull request.

`make test` runs tox across the supported Python and Django combinations.
Missing interpreters are skipped by tox, so you can run the suite locally even
if you do not have every Python version installed.

## Packaging

`make package` builds the sdist and wheel in `dist/`.

Thank you for contributing!

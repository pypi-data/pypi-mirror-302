# beepy-app-template-example

An example of the output you get when creating a new beepy app from the cookiecutter template.

## Installation

To install the application, run:

```bash
just beepy-install
```

## Usage

To run the application, use:

```bash
just run
```

## Development

To set up the development environment, initialize the application with:

```bash
just init
```

## Uninstallation

To remove the application, run:

```bash
just beepy-remove
```

## License

This project is licensed under the GPLv3 license.

## Pre-commit Hooks

This template includes pre-commit hooks for linting, formatting, and type-checking.

The hooks will run automatically on every commit, applying the specified checks and auto-formatting without asking for confirmation.

The pre-commit configuration includes:
- Black (code formatting)
- isort (import sorting)
- Flake8 (linting)
- MyPy (type checking)
- Various file checks (trailing whitespace, YAML validation, etc.)

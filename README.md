# dh_workspace

This repository is a basic Python package located under the `src/` directory.

## Development

Run the setup script to install dependencies and configure the environment:

```bash
source setup.sh
```

After running the script, tests can be executed with:

```bash
pytest
```

Format the code using [Black](https://black.readthedocs.io/) before committing:

```bash
black .
```

## Directory structure

The package code lives in `src/dh_workspace`. Game logic is implemented under
`src/dh_workspace/core/` and supporting utilities are found in
`src/dh_workspace/utils/`. Unit tests are located in the `tests/` directory.

Module-level documentation describes the available classes and functions.

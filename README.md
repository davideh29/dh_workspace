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

## Gameplay utilities

`PieceColor` is an enum representing piece colors. The `Match` class can track a
chess match for any number of players, storing the current turn, move number and
captured pieces.

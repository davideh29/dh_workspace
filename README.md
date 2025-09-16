# dh_workspace

This repository now acts as a sandbox for multiple small projects. Each
prototype lives in its own directory under `projects/` with its Python package
stored in `src/projects/<name>`.

## Development workflow

Run the setup script to install dependencies and configure the environment:

```bash
source setup.sh
```

After running the script, execute the full test suite with:

```bash
pytest
```

Format the code using [Black](https://black.readthedocs.io/) before committing:

```bash
black .
```

## Repository layout

- `src/projects/`: Python packages for each prototype. The current project is
  available at `src/projects/chess`.
- `projects/<name>/tests`: Tests and fixtures for the project named `<name>`.
- `projects/<name>/README.md`: Optional, project-specific documentation.
- `requirements.txt`: Shared dependencies for the entire workspace.

### Chess project

The existing chess prototype lives at:

- Package code: `src/projects/chess`
- Tests and resources: `projects/chess/tests`

Refer to `projects/chess/README.md` for details about this module.

## Adding a new project

1. Create a directory under `src/projects/` for the new package
   (for example `src/projects/robotics`). Add an `__init__.py` file and follow
   standard package structure.
2. Add project-specific tests under `projects/<name>/tests`. Place fixtures or
   assets next to those tests.
3. Export the module name from `src/projects/__init__.py` so it is importable as
   `projects.<name>`.
4. Document any project-specific setup in `projects/<name>/README.md`.
5. Run `black .` and `pytest` to verify the new module is formatted and tested.

Following this pattern keeps each prototype isolated while allowing them to
share tooling and dependencies.

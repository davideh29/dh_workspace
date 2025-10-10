# dh_workspace

This repository now acts as a sandbox for multiple small projects. Each
prototype lives in its own directory under `src/projects/<name>` where the
package code, tests, and any project-specific assets are grouped together.

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

- `src/projects/`: Python packages for each prototype. Current projects live at
  `src/projects/chess`, `src/projects/linear_algebra`, and
  `src/projects/reactive_store`.
- `src/projects/<name>/tests`: Tests and fixtures that live alongside the
  project code.
- `src/projects/<name>/README.md`: Optional, project-specific documentation.
- `requirements.txt`: Shared dependencies for the entire workspace.

### Chess project

The chess prototype lives at `src/projects/chess`, which now contains the
implementation, tests, and documentation in a single directory tree. Refer to
`src/projects/chess/README.md` for details about this module.

### Reactive store project

The reactive in-memory store lives at `src/projects/reactive_store`. It offers a
hierarchical key-value API that emits events to subscribers whenever keys are
set or deleted. See `src/projects/reactive_store/README.md` for usage guidance.

### Linear algebra project

The linear algebra utilities live at `src/projects/linear_algebra`. It currently
focuses on 3D rigid-body math and provides the `Transform3d` class for applying,
composing, and inverting transformations represented by translation vectors and
quaternions. Explore `src/projects/linear_algebra/README.md` for background and
examples.

## Adding a new project

1. Create a directory under `src/projects/` for the new package
   (for example `src/projects/robotics`). Add an `__init__.py` file and follow
   standard package structure.
2. Add project-specific tests under `src/projects/<name>/tests`. Place fixtures
   or assets next to those tests.
3. Export the module name from `src/projects/__init__.py` so it is importable as
   `projects.<name>`.
4. Document any project-specific setup in `src/projects/<name>/README.md`.
5. Run `black .` and `pytest` to verify the new module is formatted and tested.

Following this pattern keeps each prototype isolated while allowing them to
share tooling and dependencies.

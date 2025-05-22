This repository contains Python source code in the `src/` directory and tests in
`tests/`.

Environment Setup
-----------------
- Always run `source setup.sh` before running tests. It installs required
  packages and sets up `PYTHONPATH`.

Testing & Formatting
--------------------
- Run tests with `pytest -q`.
- Format all Python files with `black .` before committing.

Code Style
----------
- Follow PEP 8 with a maximum line length of 88 characters.
- Provide type hints on all public functions and methods.
- Include docstrings for every public module, class, and function.
- Keep functions short and focused; prefer pure functions when practical.

Code Organization
-----------------
- Gameplay code lives under `src/dh_workspace/core/`.
- Supporting utilities (configuration, logging, helper functions) live under
  `src/dh_workspace/utils/`.
- Use dataclasses for structured data.
- Always use the `PieceColor` enum for piece colors and the `PieceType` enum for
  piece identifiers.
- Use the `Match` class to track matches with any number of players.

Logging and Configuration
-------------------------
- Use the shared logger from `utils.logger` instead of creating new loggers.
- Modify global settings via `CONFIG` and `configure()` rather than introducing
  new globals.

Testing Guidance
----------------
- Add tests for any new feature or bug fix in `tests/`.
- Keep test cases focused and readable.

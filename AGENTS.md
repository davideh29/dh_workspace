This repository contains Python source code in the `src/` directory and tests in `tests/`.

Development workflow:
- Run `source setup.sh` before running tests.
- Execute tests with `pytest -q`.
- Format the code with `black .` before committing.

Style guidelines:
- Follow PEP 8 with a maximum line length of 88 characters.
- Use type hints on all public functions and methods.
- Keep code simple and prefer dataclasses for structured data.

Gameplay utilities:
- Use the `PieceColor` enum for piece colors.
- Use the `Match` class to track matches with any number of players.

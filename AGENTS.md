This repository contains Python source code under `src/projects/` with
project-specific tests stored alongside the code in `src/projects/<name>/tests`.

Rules
-----
- Run `source setup.sh` before testing. Execute `pytest -q` and format with
  `black .`.
- Follow PEP 8 (88 characters max) with type hints and docstrings. Keep
  functions short.
- Gameplay logic for the chess project lives in `src/projects/chess/core/`;
  utilities live in `src/projects/chess/utils/`. Use dataclasses, `PieceColor`,
  `PieceType` and the `Match` class for game state.
- Draw boards using `projects.chess.frontend.unicode_board` (`draw_board`,
  `draw_board_inverted`). Store board snapshots for regression tests in
  `src/projects/chess/tests/resources/`.
- Configure settings via the global `CONFIG` through `configure()` and log via
  `utils.logger`.
- Add focused tests for every feature or bug fix in the appropriate
  `src/projects/<name>/tests/` directory.

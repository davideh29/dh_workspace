This repository contains Python source code under `src/` and tests under `tests/`.

Rules
-----
- Run `source setup.sh` before testing. Execute `pytest -q` and format with `black .`.
- Follow PEP 8 (88 characters max) with type hints and docstrings. Keep functions short.
- Gameplay logic lives in `src/dh_workspace/core/`; utilities live in `src/dh_workspace/utils/`. Use dataclasses, `PieceColor`, `PieceType` and the `Match` class for game state.
- Draw boards using `frontend.unicode_board` (`draw_board`, `draw_board_inverted`). Store board snapshots for regression tests in `tests/resources/`.
- Configure settings via the global `CONFIG` through `configure()` and log via `utils.logger`.
- Add focused tests for every feature or bug fix in `tests/`.

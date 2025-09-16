# Chess prototype

This module contains the chess prototype that previously lived at the root of the
workspace.

## Layout

- Package code: `src/projects/chess`
- Core game logic: `src/projects/chess/core`
- Utilities: `src/projects/chess/utils`
- Front-end helpers: `src/projects/chess/frontend`
- Tests and fixtures: `projects/chess/tests`

## Usage

```bash
python -m projects.chess --board-width 8 --board-height 8
```

Refer to the package modules for API documentation on `Match`,
`Chessboard`, and the Unicode board rendering helpers.

import sys
from pathlib import Path

from sprite import GRID_COLS, GRID_ROWS, inspect_sprite_sheet


def main() -> int:
    if len(sys.argv) != 2:
        print("[ERROR] A sprite-sheet PNG path is required.")
        return 1

    path = Path(sys.argv[1])
    try:
        cell_w, cell_h = inspect_sprite_sheet(path)
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"[ERROR] {error}")
        return 1

    print(
        f"[OK] {path.name}: {GRID_COLS}x{GRID_ROWS} grid, "
        f"each frame is {cell_w}x{cell_h}px"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

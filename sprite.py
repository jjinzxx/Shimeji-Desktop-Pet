from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image, ImageOps, ImageTk

if TYPE_CHECKING:
    from config import Config


GRID_COLS = 4
GRID_ROWS = 4
STATE_ROWS = {"idle": 0, "walk": 1, "fall": 2, "grabbed": 3}
STATE_FRAMES = {"idle": 2, "walk": 4, "fall": 2, "grabbed": 1}


def resource_path(relative_path: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative_path


def find_sprite_sheet() -> Path:
    image_dir = resource_path("images")
    preferred = image_dir / "shimeji_sheet.png"
    if preferred.is_file():
        return preferred

    sheets = sorted(image_dir.glob("*_sheet.png"))
    if not sheets:
        sheets = sorted(image_dir.glob("*.png"))
    if not sheets and not hasattr(sys, "_MEIPASS"):
        # Source/template mode: accept a PNG placed next to build.bat.
        sheets = sorted(Path(__file__).resolve().parent.glob("*.png"))
    if not sheets:
        raise FileNotFoundError("스프라이트 시트 PNG를 찾을 수 없습니다.")
    return sheets[0]


def inspect_sprite_sheet(path: os.PathLike | str) -> tuple[int, int]:
    with Image.open(path) as image:
        width, height = image.size
        if width % GRID_COLS or height % GRID_ROWS:
            raise ValueError(
                f"스프라이트 시트 크기({width}x{height})는 "
                f"{GRID_COLS}x{GRID_ROWS} 격자로 정확히 나누어져야 합니다."
            )
        cell_w, cell_h = width // GRID_COLS, height // GRID_ROWS
        if cell_w < 1 or cell_h < 1:
            raise ValueError("스프라이트 시트의 각 칸은 최소 1x1 픽셀이어야 합니다.")
        return cell_w, cell_h


class ImageSprite:
    def __init__(self, canvas, cfg: "Config"):
        self.canvas = canvas
        self.cfg = cfg
        self.path = find_sprite_sheet()
        self._sheet = Image.open(self.path).convert("RGBA")
        cell_w, cell_h = inspect_sprite_sheet(self.path)
        self.cfg.set_sprite_size(cell_w, cell_h)
        self._cache = {}
        self._img_ref = None

    def clear_cache(self) -> None:
        self._cache.clear()

    def _get_frame(self, state: str, direction: int, frame: int):
        col = (frame // self.cfg.ANIM_TICK) % STATE_FRAMES[state]
        key = (state, direction, col, self.cfg.SCALE)
        if key not in self._cache:
            row = STATE_ROWS[state]
            width, height = self.cfg.CHAR_W, self.cfg.CHAR_H
            crop = self._sheet.crop(
                (col * width, row * height, (col + 1) * width, (row + 1) * height)
            )
            if direction == -1:
                crop = ImageOps.mirror(crop)
            if self.cfg.SCALE != 1:
                crop = crop.resize(
                    (width * self.cfg.SCALE, height * self.cfg.SCALE), Image.Resampling.NEAREST
                )
            self._cache[key] = ImageTk.PhotoImage(crop)
        return self._cache[key]

    def draw(self, state: str, direction: int, frame: int) -> None:
        image = self._get_frame(state, direction, frame)
        self._img_ref = image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=image)

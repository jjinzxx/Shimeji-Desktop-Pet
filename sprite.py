from __future__ import annotations
import math
import os
import sys
import tkinter as tk
from typing import TYPE_CHECKING
from PIL import Image, ImageOps, ImageTk

if TYPE_CHECKING:
    from config import Config


def _resource(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

class ImageSprite:
    ROW = {"idle": 0, "walk": 1, "fall": 2, "grabbed": 3}
    COLS = {"idle": 2, "walk": 4, "fall": 2, "grabbed": 1}

    def __init__(self, canvas, cfg):
        self.canvas = canvas
        self.cfg = cfg
        self._sheet = Image.open(_resource("images/shimeji_sheet.png"))
        self._cache = {}
        self._img_ref = None

    def clear_cache(self):
        self._cache.clear()

    def _get_frame(self, state, direction, frame):
        col = (frame // self.cfg.ANIM_TICK) % self.COLS[state]
        key = (state, direction, col, self.cfg.SCALE)
        if key not in self._cache:
            row = self.ROW[state]
            w, h = self.cfg.CHAR_W, self.cfg.CHAR_H
            crop = self._sheet.crop((col*w, row*h, (col+1)*w, (row+1)*h))
            if direction == -1:
                crop = ImageOps.mirror(crop)
            s = self.cfg.SCALE
            if s != 1:
                crop = crop.resize((w * s, h * s), Image.NEAREST)
            self._cache[key] = ImageTk.PhotoImage(crop)
        return self._cache[key]

    def draw(self, state, direction, frame):
        img = self._get_frame(state, direction, frame)
        self._img_ref = img
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=img)
"""A small Windows desktop pet driven by a 4x4 PNG sprite sheet."""

from __future__ import annotations

import ctypes
import random
import tkinter as tk
from tkinter import messagebox

from config import Config
from sprite import ImageSprite, find_sprite_sheet, inspect_sprite_sheet
from states import FallState, GrabbedState, IdleState, WalkState


def get_work_area(root: tk.Tk) -> tuple[int, int, int, int]:
    """Return the usable primary-monitor rectangle, excluding the taskbar."""
    if hasattr(ctypes, "windll"):
        class Rect(ctypes.Structure):
            _fields_ = [
                ("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long),
            ]

        rect = Rect()
        if ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0):
            return rect.left, rect.top, rect.right, rect.bottom
    return 0, 0, root.winfo_screenwidth(), root.winfo_screenheight()


class Shimeji:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cfg = Config()

        sheet_path = find_sprite_sheet()
        frame_width, frame_height = inspect_sprite_sheet(sheet_path)
        self.cfg.set_sprite_size(frame_width, frame_height)

        self.work_left, self.work_top, self.work_right, self.work_bottom = get_work_area(root)
        self.screen_w = self.work_right - self.work_left
        self.screen_h = self.work_bottom - self.work_top
        self.floor_y = self.work_bottom - self.cfg.DISP_H

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", self.cfg.TRANSPARENT_COLOR)
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=self.cfg.DISP_W,
            height=self.cfg.DISP_H,
            bg=self.cfg.TRANSPARENT_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        max_x = max(self.work_left, self.work_right - self.cfg.DISP_W)
        self.x = float(random.randint(self.work_left, max_x))
        self.y = float(self.floor_y)
        self.vel_y = 0.0
        self.direction = 1
        self.frame = 0

        self.sprite = ImageSprite(self.canvas, self.cfg)
        self._states = {
            "idle": IdleState(self),
            "walk": WalkState(self),
            "fall": FallState(self),
            "grabbed": GrabbedState(self),
        }
        self._state_key = "idle"
        self.state = self._states[self._state_key]
        self.state.enter()

        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._bind_events()
        self._tick()

    def change_state(self, key: str) -> None:
        self.state.exit()
        self._state_key = key
        self.state = self._states[key]
        self.state.enter()

    def on_floor(self) -> bool:
        return self.y >= self.floor_y

    def clamp_to_floor(self) -> None:
        if self.y >= self.floor_y:
            self.y = float(self.floor_y)
            self.vel_y = 0.0

    def clamp_x(self) -> None:
        right_edge = max(self.work_left, self.work_right - self.cfg.DISP_W)
        self.x = max(float(self.work_left), min(self.x, float(right_edge)))

    def _tick(self) -> None:
        self.frame += 1
        self.state.update()
        self.sprite.draw(self._state_key, self.direction, self.frame)
        self.root.geometry(
            f"{self.cfg.DISP_W}x{self.cfg.DISP_H}+{int(self.x)}+{int(self.y)}"
        )
        self.root.after(self.cfg.TICK_MS, self._tick)

    def _bind_events(self) -> None:
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<ButtonPress-3>", self._on_right_click)

    def _on_press(self, event) -> None:
        self._drag_offset_x = event.x
        self._drag_offset_y = event.y
        self.change_state("grabbed")

    def _on_drag(self, event) -> None:
        self.x = self.root.winfo_x() + event.x - self._drag_offset_x
        self.y = self.root.winfo_y() + event.y - self._drag_offset_y

    def _on_release(self, _event) -> None:
        self.clamp_x()
        if self.on_floor():
            self.clamp_to_floor()
            self.change_state("idle")
        else:
            self.vel_y = 0.0
            self.change_state("fall")

    def _on_right_click(self, _event) -> None:
        menu = tk.Menu(self.root, tearoff=0)
        scale_menu = tk.Menu(menu, tearoff=0)
        for scale in range(1, 11):
            label = f"{scale}배 ({self.cfg.CHAR_W * scale}×{self.cfg.CHAR_H * scale}px)"
            if scale == self.cfg.SCALE:
                label += " ✓"
            scale_menu.add_command(
                label=label, command=lambda value=scale: self._apply_scale(value)
            )
        menu.add_cascade(label="크기 설정", menu=scale_menu)
        menu.add_separator()
        menu.add_command(label="종료", command=self.root.destroy)
        try:
            menu.tk_popup(
                self.root.winfo_x() + self.cfg.DISP_W // 2,
                self.root.winfo_y(),
            )
        finally:
            menu.grab_release()

    def _apply_scale(self, scale: int) -> None:
        self.cfg.set_scale(scale)
        self.sprite.clear_cache()
        self.canvas.config(width=self.cfg.DISP_W, height=self.cfg.DISP_H)
        self.floor_y = self.work_bottom - self.cfg.DISP_H
        if self.y > self.floor_y:
            self.y = float(self.floor_y)
        self.clamp_x()


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    try:
        Shimeji(root)
        root.deiconify()
        root.mainloop()
    except Exception as error:
        messagebox.showerror("Shimeji 실행 오류", str(error), parent=root)
        root.destroy()


if __name__ == "__main__":
    main()

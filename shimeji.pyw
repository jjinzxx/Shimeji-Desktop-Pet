"""
    Shimeji-Desktop-Pet
    파일: shimeji.pyw
    제작자: jjinzxx
    깃허브: https://github.com/jjinzxx/Shimeji-Desktop-Pet
    제작일: 2026-06-25
    설명: 스프라이트 이미지를 넣고 직접 시메지 프로그램을 만들어보세요.
"""

import tkinter as tk
import random
import math

from config import Config
from sprite import ImageSprite
from states import IdleState, WalkState, FallState, GrabbedState


class Shimeji:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cfg = Config()

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        self.floor_y  = self.screen_h - self.cfg.TASKBAR_H - self.cfg.DISP_H

        # 투명 오버레이 창
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

        # 초기 위치
        self.x: float = random.randint(100, self.screen_w - 100)
        self.y: float = float(self.floor_y)
        self.vel_y: float = 0.0
        self.direction: int = 1          # 1=오른쪽, -1=왼쪽
        self.frame: int = 0

        self.sprite = ImageSprite(self.canvas, self.cfg)

        # 상태머신
        self._states = {
            "idle":    IdleState(self),
            "walk":    WalkState(self),
            "fall":    FallState(self),
            "grabbed": GrabbedState(self),
        }
        self._state_key = "idle"
        self.state = self._states["idle"]
        self.state.enter()          # 초기 상태 enter() 명시 호출

        # 드래그용
        self._drag_offset_x = 0
        self._drag_offset_y = 0

        self._bind_events()
        self._tick()

    # ── 상태 전환 ──────────────────────────────────────────────────────────
    def change_state(self, key: str):
        self.state.exit()
        self._state_key = key
        self.state = self._states[key]
        self.state.enter()

    # ── 위치 헬퍼 ──────────────────────────────────────────────────────────
    def on_floor(self) -> bool:
        return self.y >= self.floor_y

    def clamp_to_floor(self):
        if self.y > self.floor_y:
            self.y = float(self.floor_y)
            self.vel_y = 0.0

    def clamp_x(self):
        self.x = max(0.0, min(self.x, float(self.screen_w - self.cfg.DISP_W)))

    # ── 메인 루프 ──────────────────────────────────────────────────────────
    def _tick(self):
        self.root.after(self.cfg.TICK_MS, self._tick)
        self.frame += 1
        self.state.update()
        self.sprite.draw(self._state_key, self.direction, self.frame)
        self.root.geometry(
            f"{self.cfg.DISP_W}x{self.cfg.DISP_H}+{int(self.x)}+{int(self.y)}"
        )

    # ── 이벤트 ─────────────────────────────────────────────────────────────
    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        self.canvas.bind("<B1-Motion>",        self._on_drag)
        self.canvas.bind("<ButtonRelease-1>",  self._on_release)
        self.canvas.bind("<ButtonPress-3>",    self._on_right_click)

    def _on_press(self, event):
        self._drag_offset_x = event.x
        self._drag_offset_y = event.y
        self.change_state("grabbed")

    def _on_drag(self, event):
        self.x = self.root.winfo_x() + event.x - self._drag_offset_x
        self.y = self.root.winfo_y() + event.y - self._drag_offset_y

    def _on_release(self, _event):
        if not self.on_floor():
            self.vel_y = 0.0
            self.change_state("fall")
        else:
            self.change_state("idle")

    def _on_right_click(self, _event):
        menu = tk.Menu(self.root, tearoff=0)

        scale_menu = tk.Menu(menu, tearoff=0)
        for s in range(1, 11):
            label = f"{s}×  ({self.cfg.CHAR_W*s}×{self.cfg.CHAR_H*s}px)"
            if s == self.cfg.SCALE:
                label += "  ✓"
            scale_menu.add_command(
                label=label,
                command=lambda v=s: self._apply_scale(v),
            )
        menu.add_cascade(label="배율 설정", menu=scale_menu)
        menu.add_separator()
        menu.add_command(label="종료", command=self.root.destroy)
        menu.tk_popup(
            self.root.winfo_x() + self.cfg.DISP_W // 2,
            self.root.winfo_y(),
        )

    def _apply_scale(self, scale: int):
        self.cfg.set_scale(scale)
        self.sprite.clear_cache()
        self.canvas.config(width=self.cfg.DISP_W, height=self.cfg.DISP_H)
        self.floor_y = self.screen_h - self.cfg.TASKBAR_H - self.cfg.DISP_H
        if self.y > self.floor_y:
            self.y = float(self.floor_y)
        self.clamp_x()


def main():
    root = tk.Tk()
    Shimeji(root)
    root.mainloop()


if __name__ == "__main__":
    main()

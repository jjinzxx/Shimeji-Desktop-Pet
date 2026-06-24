from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shimeji import Shimeji


class _BaseState:
    def __init__(self, host: "Shimeji"):
        self.host = host

    def enter(self): pass
    def update(self): pass
    def exit(self): pass


# ── Idle ────────────────────────────────────────────────────────────────────

class IdleState(_BaseState):
    def enter(self):
        cfg = self.host.cfg
        self._timer = random.randint(*cfg.IDLE_DURATION)

    def update(self):
        self._timer -= 1
        if self._timer <= 0:
            self.host.direction = random.choice([-1, 1])
            self.host.change_state("walk")


# ── Walk ────────────────────────────────────────────────────────────────────

class WalkState(_BaseState):
    def enter(self):
        cfg = self.host.cfg
        self._timer = random.randint(*cfg.WALK_DURATION)

    def update(self):
        host = self.host
        host.x += host.cfg.WALK_SPEED * host.direction
        host.clamp_x()

        if host.x <= 0:
            host.direction = 1
        elif host.x >= host.screen_w - host.cfg.DISP_W:
            host.direction = -1

        self._timer -= 1
        if self._timer <= 0:
            host.change_state("idle")


# ── Fall ────────────────────────────────────────────────────────────────────

class FallState(_BaseState):
    def enter(self):
        self.host.vel_y = 0.0

    def update(self):
        host = self.host
        host.vel_y = min(host.vel_y + host.cfg.GRAVITY, host.cfg.MAX_FALL_SPEED)
        host.y += host.vel_y

        if host.on_floor():
            host.clamp_to_floor()
            host.change_state("idle")


# ── Grabbed ─────────────────────────────────────────────────────────────────

class GrabbedState(_BaseState):
    def update(self):
        pass

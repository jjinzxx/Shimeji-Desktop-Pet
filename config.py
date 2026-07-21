class Config:
    """Runtime settings for the desktop pet."""

    # These are replaced automatically with sheet_width/4 and sheet_height/4.
    CHAR_W: int = 16
    CHAR_H: int = 20
    SCALE: int = 5
    DISP_W: int = CHAR_W * SCALE
    DISP_H: int = CHAR_H * SCALE

    TRANSPARENT_COLOR: str = "#010101"
    TICK_MS: int = 16
    ANIM_TICK: int = 12
    WALK_SPEED: float = 1.0
    GRAVITY: float = 0.6
    MAX_FALL_SPEED: float = 14.0
    IDLE_DURATION = (60, 200)
    WALK_DURATION = (80, 200)

    def set_sprite_size(self, width: int, height: int) -> None:
        self.CHAR_W = width
        self.CHAR_H = height
        self._update_display_size()

    def set_scale(self, scale: int) -> None:
        self.SCALE = scale
        self._update_display_size()

    def _update_display_size(self) -> None:
        self.DISP_W = self.CHAR_W * self.SCALE
        self.DISP_H = self.CHAR_H * self.SCALE

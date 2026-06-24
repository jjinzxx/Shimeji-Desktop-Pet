class Config:
    # 스프라이트 시트 셀 크기 (스프라이트 시트 크기x, 셀 하나의 크기)
    CHAR_W: int = 16
    CHAR_H: int = 20

    # 화면 표시 배율 (원본 셀 크기가 작다면 배율을 올리세요)
    SCALE: int = 5

    # 실제 표시 크기 (스프라이트 시트 크기)
    DISP_W: int = CHAR_W * SCALE   # 64
    DISP_H: int = CHAR_H * SCALE   # 80

    def set_scale(self, scale: int):
        self.SCALE = scale
        self.DISP_W = self.CHAR_W * scale
        self.DISP_H = self.CHAR_H * scale

    # 투명색 (Windows -transparentcolor 용)
    TRANSPARENT_COLOR: str = "#010101"

    # 화면 하단 여백 (작업표시줄 높이 근사값)
    TASKBAR_H: int = 48

    # 틱 간격 ms  (~60 fps)
    TICK_MS: int = 16

    # 애니메이션 프레임당 틱 수 (클수록 느린 애니메이션)
    # 12틱 × 16ms = 192ms/프레임 ≈ 초당 5장
    ANIM_TICK: int = 12

    # 걷기 속도 (픽셀/틱)
    WALK_SPEED: float = 1.0

    # 중력 가속도 (픽셀/틱²)
    GRAVITY: float = 0.6

    # 최대 낙하 속도
    MAX_FALL_SPEED: float = 14.0

    # idle 유지 틱 범위 (min, max)
    IDLE_DURATION = (60, 200)

    # 걷기 유지 틱 범위
    WALK_DURATION = (80, 200)


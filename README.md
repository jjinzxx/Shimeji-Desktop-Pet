# Shimeji-Desktop-Pet

데스크탑 위를 돌아다니는 픽셀 캐릭터 시메지 프로그램입니다.  
스프라이트 시트 하나만 교체하면 어떤 캐릭터든 올릴 수 있어요.

<br>

> 제작자: jjinzxx <br>
> 제작일: 2026-06-25 <br>
> GitHub: [Shimeji-Desktop-Pet](https://github.com/jjinzxx/Shimeji-Desktop-Pet) <br>


<br>

## 실행 방법

### A. EXE 파일로 실행 (Python 불필요)

`dist` 폴더 안의 `.exe` 파일을 더블클릭하면 바로 실행됩니다.  
다른 컴퓨터로 옮길 때 이 파일 하나만 복사하면 됩니다.

### B. Python으로 직접 실행

```bash
pip install pillow
python shimeji.pyw
```

<br><br>

## 조작법

| 입력 | 동작 |
|------|------|
| 왼쪽 버튼 드래그 | 캐릭터 잡아서 이동 (놓으면 낙하) |
| 오른쪽 버튼 클릭 | 메뉴 열기 |

**우클릭 메뉴**
- **캐릭터 변경** — 시트가 2개 이상일 때 표시
- **배율 설정** — 1배 ~ 10배 크기 조절
- **종료**

<br><br>

## EXE 직접 빌드하기

`build.bat`을 더블클릭하면 EXE 이름을 입력하는 창이 열립니다.  
원하는 이름을 입력하면 `dist\<입력한이름>.exe`가 생성됩니다.

```
EXE 파일 이름을 입력하세요 (예: MyShimeji): MyShimeji
→ dist\MyShimeji.exe 생성 완료
```

필요한 패키지는 빌드 시 자동으로 설치됩니다.

```bash
pip install pillow pyinstaller
```

<br><br>

## 캐릭터 추가하기

`images` 폴더에 `이름_sheet.png` 형식으로 스프라이트 시트를 넣으면  
우클릭 → **캐릭터 변경** 메뉴에 자동으로 표시됩니다.

<br><br>

## 스프라이트 시트 규칙

시트는 **가로 4칸 × 세로 4행** 격자로 만들어야 합니다.

| 행 | 동작 | 사용 칸 수 |
|----|------|-----------|
| 1행 | idle (가만히) | 앞 2칸 |
| 2행 | walk (걷기) | 4칸 전부 |
| 3행 | fall (낙하) | 앞 2칸 |
| 4행 | grabbed (잡힘) | 1칸 |

- **칸 크기는 자유**입니다. 프로그램이 `시트 전체 크기 ÷ 4`로 자동 계산합니다.
- 예시: 한 칸 32×40px → 시트 전체 128×160px

> **칸 수를 바꾸고 싶을 때** → `sprite.py` 상단의 `COLS` 딕셔너리 수정
> ```python
> COLS = {"idle": 2, "walk": 4, "fall": 2, "grabbed": 1}
> ```
> 격자가 4×4가 아닐 때는 `CHAR_W / CHAR_H` 자동 계산 기준도 함께 수정하세요.

<br><br>

## 아이콘 설정

프로젝트 폴더에 `icon.ico`를 넣으면 창 아이콘과 EXE 아이콘에 자동 적용됩니다.

<br><br>

## 세부 조정 (config.py)

| 항목 | 설명 |
|------|------|
| `SCALE` | 기본 확대 배율 (우클릭으로도 변경 가능) |
| `ANIM_TICK` | 클수록 애니메이션이 느려짐 |
| `WALK_SPEED` | 걷는 속도 |
| `GRAVITY` | 낙하 가속도 |
| `TASKBAR_H` | 바닥(작업표시줄) 높이 — 캐릭터가 바닥에 안 맞을 때 조절 |

<br><br>

## 필요 환경

- Python 3.x (B 방법 또는 빌드 시)
- [Pillow](https://pypi.org/project/pillow/)
- [PyInstaller](https://pypi.org/project/pyinstaller/) (EXE 빌드 시)

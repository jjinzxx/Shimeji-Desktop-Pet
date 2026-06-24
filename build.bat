@echo off
chcp 65001 > nul

set /p EXE_NAME=EXE 파일 이름을 입력하세요 (예: MyShimeji):

if "%EXE_NAME%"=="" (
    echo 이름을 입력하지 않았습니다. 종료합니다.
    pause
    exit /b 1
)

echo.
echo [1/2] 의존 패키지 설치 중...
python -m pip install pillow pyinstaller

echo.
echo [2/2] 빌드 중: %EXE_NAME%.exe
if exist "icon.ico" (
    python -m PyInstaller --onefile --windowed --name "%EXE_NAME%" --add-data "images;images" --add-data "icon.ico;." --icon "icon.ico" shimeji.pyw
) else (
    python -m PyInstaller --onefile --windowed --name "%EXE_NAME%" --add-data "images;images" shimeji.pyw
)

echo.
if exist "dist\%EXE_NAME%.exe" (
    echo 빌드 완료: dist\%EXE_NAME%.exe
) else (
    echo 빌드 실패. 위 오류 메시지를 확인하세요.
)
pause

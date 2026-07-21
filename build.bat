@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

rem This file intentionally uses ASCII only so every Windows code page can parse it.
set "SPRITE_SHEET="
set /a "PNG_COUNT=0"
for %%F in (*.png) do (
    set /a "PNG_COUNT+=1"
    set "SPRITE_SHEET=%%F"
)

if !PNG_COUNT! EQU 0 (
    echo [ERROR] No PNG file was found.
    echo Put exactly one sprite-sheet PNG next to build.bat.
    goto :fail
)
if !PNG_COUNT! GTR 1 (
    echo [ERROR] More than one PNG file was found.
    echo Keep only the sprite sheet PNG next to build.bat and try again.
    goto :fail
)

set "EXE_NAME=ShimejiPet"
set /p "EXE_NAME=EXE name [ShimejiPet]: "
call :trim_name
if not defined EXE_NAME set "EXE_NAME=ShimejiPet"

call :find_python
if not defined PYTHON_EXE call :install_python
if not defined PYTHON_EXE (
    echo [ERROR] Python could not be installed automatically.
    echo Check your internet connection and try again.
    goto :fail
)

echo.
echo [1/3] Checking !SPRITE_SHEET!...
"!PYTHON_EXE!" validate_sprite.py "!SPRITE_SHEET!"
if errorlevel 1 goto :fail

echo.
echo [2/3] Installing build packages...
"!PYTHON_EXE!" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto :fail

echo.
echo [3/3] Building !EXE_NAME!.exe...
if exist "icon.ico" (
    "!PYTHON_EXE!" -m PyInstaller --noconfirm --clean --onefile --windowed --name "!EXE_NAME!" --add-data "!SPRITE_SHEET!;images" --icon "icon.ico" shimeji.pyw
) else (
    "!PYTHON_EXE!" -m PyInstaller --noconfirm --clean --onefile --windowed --name "!EXE_NAME!" --add-data "!SPRITE_SHEET!;images" shimeji.pyw
)
if errorlevel 1 goto :fail

if not exist "dist\!EXE_NAME!.exe" (
    echo [ERROR] PyInstaller finished without creating the EXE.
    goto :fail
)

echo.
echo [DONE] dist\!EXE_NAME!.exe
pause
exit /b 0

:fail
echo.
echo Build failed. Review the message above.
pause
exit /b 1

:trim_name
if not defined EXE_NAME exit /b 0
if "%EXE_NAME:~0,1%"==" " set "EXE_NAME=%EXE_NAME:~1%"& goto trim_name
if "%EXE_NAME:~-1%"==" " set "EXE_NAME=%EXE_NAME:~0,-1%"& goto trim_name
exit /b 0

:find_python
set "PYTHON_EXE="
for /f "usebackq delims=" %%P in (`py -3 -c "import sys; assert sys.version_info ^>= (3, 9); print(sys.executable)" 2^>nul`) do set "PYTHON_EXE=%%P"
if defined PYTHON_EXE exit /b 0
for /f "usebackq delims=" %%P in (`python -c "import sys; assert sys.version_info ^>= (3, 9); print(sys.executable)" 2^>nul`) do set "PYTHON_EXE=%%P"
if defined PYTHON_EXE exit /b 0
for %%V in (313 312 311 310) do (
    if not defined PYTHON_EXE if exist "!LocalAppData!\Programs\Python\Python%%V\python.exe" set "PYTHON_EXE=!LocalAppData!\Programs\Python\Python%%V\python.exe"
)
exit /b 0

:install_python
echo.
echo Python 3 was not found. Installing it for the current user...
where winget >nul 2>nul
if not errorlevel 1 (
    winget install --id Python.Python.3.12 --exact --scope user --silent --disable-interactivity --accept-package-agreements --accept-source-agreements
    call :find_python
    if defined PYTHON_EXE exit /b 0
)

echo winget is unavailable. Downloading Python from python.org...
set "PYTHON_INSTALLER=!TEMP!\shimeji-python-installer.exe"
set "PYTHON_ARCH=amd64"
if /i "!PROCESSOR_ARCHITECTURE!"=="ARM64" set "PYTHON_ARCH=arm64"
if /i "!PROCESSOR_ARCHITECTURE!"=="x86" set "PYTHON_ARCH=win32"
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.10/python-3.12.10-!PYTHON_ARCH!.exe"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing $env:PYTHON_URL -OutFile $env:PYTHON_INSTALLER"
if errorlevel 1 exit /b 1

start /wait "" "!PYTHON_INSTALLER!" /quiet InstallAllUsers=0 TargetDir="!LocalAppData!\Programs\Python\Python312" PrependPath=1 Include_launcher=1 Include_pip=1 Include_test=0 Shortcuts=0
set "INSTALL_RESULT=!ERRORLEVEL!"
if exist "!PYTHON_INSTALLER!" del /q "!PYTHON_INSTALLER!"
if not "!INSTALL_RESULT!"=="0" exit /b 1

call :find_python
exit /b 0

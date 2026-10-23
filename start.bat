@echo off
setlocal
cd /d "%~dp0"

set "PYEXE="
where python >nul 2>nul && set "PYEXE=python"
if not defined PYEXE (
  where py >nul 2>nul && set "PYEXE=py"
)
if not defined PYEXE (
  if exist "%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" (
    set "PYEXE=%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
  )
)
if not defined PYEXE (
  echo [ERROR] Python not found. Please install Python 3 or edit this file.
  pause
  exit /b 1
)

echo.
echo   Ink Scroll of Jinling - Local Preview
echo   -------------------------------------
echo   Starting local server on http://127.0.0.1:8080/
echo   Press Ctrl+C to stop.
echo.

start "" http://127.0.0.1:8080/
"%PYEXE%" serve.py 8080

echo.
echo Server stopped.
pause

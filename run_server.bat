@echo off
REM Use ASCII-only lines so cmd.exe does not misparse UTF-8 multibyte chars as commands.
echo Django dev server launcher
echo --------------------------

cd /d "%~dp0myproject"
if errorlevel 1 (
  echo ERROR: could not cd to myproject
  pause
  exit /b 1
)

call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
  echo ERROR: could not activate venv
  pause
  exit /b 1
)

echo Running migrations...
python manage.py migrate
if errorlevel 1 (
  echo ERROR: migrate failed
  pause
  exit /b 1
)

echo Starting dev server...
python manage.py runserver
REM python manage.py runserver 8080

pause

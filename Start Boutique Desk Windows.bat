@echo off
cd /d "%~dp0"
title Boutique Desk - Local App
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 local_server.py
) else (
  python local_server.py
)
if errorlevel 1 (
  echo.
  echo Could not start Boutique Desk. Make sure Python 3 is installed.
  echo Download Python from python.org if needed, then try again.
  pause
)

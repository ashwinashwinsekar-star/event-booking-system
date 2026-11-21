@echo off
cd /d "%~dp0"
echo ========================================================
echo   Pushing EventHub Project to GitHub
echo ========================================================
echo Remote: https://github.com/ashwinashwinsekar-star/event-booking-system.git
echo.
git push -u origin main
echo.
pause

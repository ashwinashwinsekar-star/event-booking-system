@echo off
cd /d "%~dp0"
echo ========================================================
echo   Starting EventHub Management and Ticket Booking System
echo ========================================================
start "EventHub Backend (Django)" "%~dp0run_backend.bat"
start "EventHub Frontend (React+Vite)" "%~dp0run_frontend.bat"
echo.
echo Both servers are launching in separate windows...
echo Waiting 3 seconds before opening your browser...
timeout /t 3 /nobreak >nul
start http://localhost:5173
echo.
echo - Frontend URL: http://localhost:5173
echo - Backend API:  http://localhost:8000/api/v1/
echo - Admin Portal: http://localhost:8000/admin/
echo.
echo Default Demo Accounts:
echo - Attendee:  attendee@eventhub.com  / Attendee@123
echo - Organizer: organizer@eventhub.com / Organizer@123
echo - Admin:     admin@eventhub.com     / Admin@123
echo.

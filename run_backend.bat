@echo off
cd /d "%~dp0"
echo ====================================================
echo Starting EventHub Django REST Backend on http://localhost:8000 ...
echo ====================================================
set PATH=C:\Users\ASHWIN\AppData\Local\Programs\Python\Python312;C:\Users\ASHWIN\AppData\Local\Programs\Python\Python312\Scripts;%PATH%
"C:\Users\ASHWIN\AppData\Local\Programs\Python\Python312\python.exe" manage.py runserver 0.0.0.0:8000
pause

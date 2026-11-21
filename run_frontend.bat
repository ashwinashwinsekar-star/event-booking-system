@echo off
cd /d "%~dp0frontend"
echo ====================================================
echo Starting EventHub React Frontend on http://localhost:5173 ...
echo ====================================================
set PATH=C:\Users\ASHWIN\AppData\Local\Programs\Python\Python312\Lib\site-packages\nodejs;C:\Users\ASHWIN\AppData\Local\Programs\Python\Python312;C:\Users\ASHWIN\AppData\Local\Programs\Python\Python312\Scripts;%PATH%
npm run dev -- --host 0.0.0.0 --port 5173
pause

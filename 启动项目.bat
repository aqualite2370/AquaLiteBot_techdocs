@echo off
chcp 65001 >nul
title Tech Docs Startup

echo ========================================
echo    Tech Docs Project - Startup Script
echo ========================================
echo.

:: Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo OK: Python found
echo.

:: Check Node.js
echo [2/5] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js
    pause
    exit /b 1
)
echo OK: Node.js found
echo.

:: Install backend dependencies
echo [3/5] Installing backend dependencies...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
cd ..
echo OK: Backend dependencies installed
echo.

:: Install frontend dependencies
echo [4/5] Installing frontend dependencies...
cd frontend
if not exist "node_modules" (
    echo Installing npm packages...
    call npm install
)
cd ..
echo OK: Frontend dependencies installed
echo.

:: Start services
echo [5/5] Starting services...
echo.
echo ========================================
echo    Services Starting...
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo WARNING: Closing this window will stop all services
echo ========================================
echo.

:: Start backend in new window
start "FastAPI Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && python main.py"

:: Wait for backend
timeout /t 3 /nobreak >nul

:: Start frontend in new window
start "Vue Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

:: Wait for frontend
timeout /t 5 /nobreak >nul

:: Open browser
echo Opening browser...
start http://localhost:3000

echo.
echo OK: All services started!
echo.
echo Press any key to close this window (services will continue running)...
pause >nul
